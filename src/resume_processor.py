import os
import pandas as pd
from cerebras.cloud.sdk import Cerebras
import json
import re
from typing import Dict, List, Optional
import time
from datetime import datetime

class ResumeProcessor:
    def __init__(self, api_key: str):
        """Initialize the resume processor with Cerebras API.""" # 可换用其他API
        self.client = Cerebras(api_key=api_key)
        self.model = "llama-4-scout-17b-16e-instruct"  # 可换用其他model
        self.processed_count = 0
        self.start_time = time.time()
        
    def extract_resume_info(self, resume_text: str, user_name: str) -> Dict:
        """Extract structured information from resume text using Cerebras API."""
        
        prompt = f"""
你是一个专业的简历信息提取助手。请从以下基金经理简历中提取结构化信息。

简历内容：
{resume_text}

请按照以下格式提取信息，如果某项信息不存在，请用"-"表示：

1. 基本信息：
- 性别（男/女）
- 学历（取最高学历：本科/硕士/博士等）
- 毕业院校（最高学历的毕业院校）

2. 教育经历（格式：大学名称|专业名称|学位名称|开始时间|结束时间）：
- 时间格式用yyyymm，如果只有年份，用01月表示（如201901）
- 如果信息缺失，用"-"替代
- 按学位级别分类：学士、硕士、博士、其他
- 函授算作学士学位
- 如果简历只有某一项学历，其他项留空

3. 工作经历（格式：公司名称|职位名称|开始时间|结束时间）：
- 时间格式用yyyymm，如果只有年份，用01月表示
- 如果信息缺失，用"-"替代
- 最多提取5个工作经历

4. 其他特征（直接摘录原文文字，不做修改）：
- certification：获取的证书、证明等
- charity：参与慈善活动
- prize：获奖，包括业内/业外获奖，行业、监管机构认可等
- hobby：个人爱好
- expert_in：擅长领域，包括行业从业经验，研究领域等
- writings：有著作，包括学术文章、书籍、媒体报纸等
- part_time_job：其他公司、行业组织等的兼职等
- social_activities：社会活动

5. 其他信息：简历中去除以上已经识别出的项目的内容
- 请仅保留未出现在上述“基本信息”、“教育经历”、“工作经历”及“其他特征”各项中的内容。
- 若信息完全被上述提取项覆盖，请填"-"

请以JSON格式返回结果：
{{
  "basic_info": {{
    "gender": "",
    "education": "",
    "graduate_school": ""
  }},
  "education_history": {{
    "bachelor": "",
    "master": "",
    "doctor": "",
    "other": ""
  }},
  "work_history": [
    "公司名称|职位名称|开始时间|结束时间"
  ],
  "other_features": {{
    "certification": "",
    "charity": "",
    "prize": "",
    "hobby": "",
    "expert_in": "",
    "writings": "",
    "part_time_job": "",
    "social_activities": ""
  }},
  "other": ""
}}
        """
        
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {"role": "user", "content": prompt}
                ],
                model=self.model,
                max_tokens=2000,
                temperature=0.1
            )
            
            response_text = chat_completion.choices[0].message.content
            
            # Try to extract JSON from response
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
                return json.loads(json_str)
            else:
                print(f"  Warning: Could not parse JSON from response for {user_name}")
                return self._get_empty_structure()
                
        except Exception as e:
            print(f"  Error: API call failed for {user_name}: {str(e)}")
            return self._get_empty_structure()
    
    def _get_empty_structure(self) -> Dict:
        """Return empty structure when processing fails."""
        return {
            "basic_info": {
                "gender": "-",
                "education": "-",
                "graduate_school": "-"
            },
            "education_history": {
                "bachelor": "-",
                "master": "-",
                "doctor": "-",
                "other": "-"
            },
            "work_history": [],
            "other_features": {
                "certification": "-",
                "charity": "-",
                "prize": "-",
                "hobby": "-",
                "expert_in": "-",
                "writings": "-",
                "part_time_job": "-",
                "social_activities": "-"
            },
            "other": "-"
        }
    
    def _print_progress(self, current: int, total: int, user_name: str):
        """Print progress information."""
        elapsed = time.time() - self.start_time
        if current > 0:
            avg_time = elapsed / current
            remaining = (total - current) * avg_time
            eta_str = f"ETA: {remaining/60:.1f} min"
        else:
            eta_str = "ETA: calculating..."
        
        print(f"[{current}/{total}] Processing: {user_name} | Elapsed: {elapsed/60:.1f} min | {eta_str}")
    
    def process_dataframe(self, df: pd.DataFrame, start_idx: int = 0, end_idx: Optional[int] = None, 
                         checkpoint_interval: int = 50) -> pd.DataFrame:
        """Process the entire dataframe and fill in structured information."""
        
        if end_idx is None:
            end_idx = len(df)
            
        processed_df = df.copy()
        
        # Convert columns to object type to avoid dtype warnings
        string_columns = ['gender', 'education', 'graduate_school', '教育1', '教育2', '教育3', 
                         '工作1', '工作2', '工作3', '工作4', '工作5', 'certification', 'charity', 
                         'prize', 'hobby', 'expert_in', 'writings', 'part-time_job', 
                         'social_activities', 'OTHER']
        
        for col in string_columns:
            if col in processed_df.columns:
                processed_df[col] = processed_df[col].astype('object')
        
        records_with_resume = 0
        
        for idx in range(start_idx, min(end_idx, len(df))):
            row = df.iloc[idx]
            user_id = row['user_id']
            user_name = row['user_name']
            resume_minfo = str(row['resume_minfo']) if pd.notna(row['resume_minfo']) else ""
            resume_pinfo = str(row['resume_pinfo']) if pd.notna(row['resume_pinfo']) else ""
            
            self._print_progress(idx - start_idx + 1, end_idx - start_idx, user_name)
            
            # Skip if no resume information
            if not resume_minfo or resume_minfo == "-" or resume_minfo == "nan":
                print(f"  → Skipping - no resume information")
                continue
            
            records_with_resume += 1
            
            # Combine resume information
            full_resume = f"{resume_minfo} {resume_pinfo}".strip()
            
            # Extract information using AI
            extracted_info = self.extract_resume_info(full_resume, user_name)
            
            # Update basic info if needed
            cd_changed = False
            if pd.isna(row['gender']) and extracted_info['basic_info']['gender'] != "-":
                processed_df.loc[idx, 'gender'] = extracted_info['basic_info']['gender']
                cd_changed = True
                
            if pd.isna(row['education']) and extracted_info['basic_info']['education'] != "-":
                processed_df.loc[idx, 'education'] = extracted_info['basic_info']['education']
                cd_changed = True
                
            if pd.isna(row['graduate_school']) and extracted_info['basic_info']['graduate_school'] != "-":
                processed_df.loc[idx, 'graduate_school'] = extracted_info['basic_info']['graduate_school']
                cd_changed = True
                
            if cd_changed:
                processed_df.loc[idx, 'CD_change'] = 1
                print(f"  → Updated basic info (C/D columns)")
            
            # Fill education history
            education_cols = ['教育1', '教育2', '教育3']
            edu_count = 0
            print(extracted_info['education_history'])
            education_levels = ['bachelor', 'master', 'doctor']
            
            # Handle both dict and list formats for education_history
            if isinstance(extracted_info['education_history'], dict):
                for i, level in enumerate(education_levels):
                    edu = extracted_info['education_history'].get(level, "")
                    if edu and edu != "-":
                        processed_df.loc[idx, education_cols[i]] = edu
                        edu_count += 1
            elif isinstance(extracted_info['education_history'], list):
                # If it's a list, try to use the first few entries
                for i, edu in enumerate(extracted_info['education_history'][:3]):
                    if edu and edu != "-":
                        processed_df.loc[idx, education_cols[i]] = edu
                        edu_count += 1

            if edu_count > 0:
                print(f"  → Added {edu_count} education record(s)")
            
            # Fill work history
            work_cols = ['工作1', '工作2', '工作3', '工作4', '工作5']
            work_count = 0
            for i, work in enumerate(extracted_info['work_history'][:5]):
                if work and work != "-":
                    processed_df.loc[idx, work_cols[i]] = work
                    work_count += 1
            if work_count > 0:
                print(f"  → Added {work_count} work record(s)")
            
            # Fill other features
            feature_count = 0
            for feature, value in extracted_info['other_features'].items():
                if value and value != "-":
                    processed_df.loc[idx, feature] = value
                    feature_count += 1
            if feature_count > 0:
                print(f"  → Added {feature_count} feature(s)")
            
            # Fill other information
            if extracted_info['other'] and extracted_info['other'] != "-":
                processed_df.loc[idx, 'OTHER'] = extracted_info['other']
                print(f"  → Added other information")
            
            self.processed_count += 1
            
            # Save checkpoint periodically
            if (idx - start_idx + 1) % checkpoint_interval == 0:
                checkpoint_file = f"checkpoint_{idx+1}.xlsx"
                processed_df.to_excel(checkpoint_file, index=False)
                print(f"  → Checkpoint saved: {checkpoint_file}")
            
            # Rate limiting
            time.sleep(0.3)  # Slightly faster than before
        
        print(f"\n📊 Processing Summary:")
        print(f"- Total records examined: {end_idx - start_idx}")
        print(f"- Records with resume data: {records_with_resume}")
        print(f"- Records successfully processed: {self.processed_count}")
        
        return processed_df

def main():
    print("🚀 Starting Full Resume Processing Pipeline")
    print(f"⏰ Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    # Set up API key - get from environment variable
    api_key = os.environ.get("CEREBRAS_API_KEY")   # or replace it with your API key 
    if not api_key:
        print("❌ Error: Please set CEREBRAS_API_KEY environment variable")
        print("Example: export CEREBRAS_API_KEY='your_api_key_here'")
        return
    
    # File paths - update these to your local files
    input_file = "example_data/manager_cv.xlsx"  # Update this path
    output_file = "output/processed_manager_cv.xlsx"  # Update this path
    
    try:
        # Load the Excel file
        print("📂 Loading Excel file...")
        df = pd.read_excel(input_file)
        print(f"✅ Loaded {len(df)} records")
        
        # Count records with resume data
        resume_count = df['resume_minfo'].notna().sum() - (df['resume_minfo'] == '-').sum()
        print(f"📋 Records with resume data: {resume_count}")
        print(f"⏱️  Estimated processing time: {resume_count * 0.3 / 60:.1f} minutes")
        
        # Initialize processor
        processor = ResumeProcessor(api_key)
        
        # Process ALL records
        print("\n🔄 Starting processing...")
        processed_df = processor.process_dataframe(df, checkpoint_interval=100)
        
        # Save the final processed dataframe
        print(f"\n💾 Saving final processed data to {output_file}...")
        processed_df.to_excel(output_file, index=False)
        print("✅ Processing completed successfully!")
        
        # Show final summary
        changes_count = processed_df['CD_change'].sum()
        total_time = time.time() - processor.start_time
        
        print(f"\n📈 Final Summary:")
        print(f"- Total records: {len(processed_df)}")
        print(f"- Records with C/D updates: {changes_count}")
        print(f"- Total processing time: {total_time/60:.1f} minutes")
        print(f"- Average time per record: {total_time/len(df):.2f} seconds")
        print(f"🎉 Output saved to: {output_file}")
        
    except KeyboardInterrupt:
        print("\n⚠️  Processing interrupted by user")
        print("💾 Check for checkpoint files in the directory")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

