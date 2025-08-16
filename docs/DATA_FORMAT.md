# Data Format Documentation

## Input Excel File Format

The input Excel file should contain the following columns:

### Required Columns

| Column Name | Type | Description | Example |
|-------------|------|-------------|---------|
| `user_id` | String | Unique identifier for each person | P00000007 |
| `user_name` | String | Person's name | 张三 |
| `resume_minfo` | String | Main resume information | 详细的简历内容... |
| `resume_pinfo` | String | Additional resume information | 补充简历信息... |

### Optional Columns (will be filled if missing)

| Column Name | Type | Description | Example |
|-------------|------|-------------|---------|
| `gender` | String | Gender (男/女) | 男 |
| `education` | String | Highest education level | 博士 |
| `graduate_school` | String | School of highest degree | 清华大学 |

### Output Columns (added by processing)

| Column Name | Type | Description | Format |
|-------------|------|-------------|---------|
| `CD_change` | Integer | Flag if basic info was updated | 0 or 1 |
| `教育1` | String | Bachelor's degree info | 大学名称\|专业名称\|学位名称\|开始时间\|结束时间 |
| `教育2` | String | Master's degree info | 大学名称\|专业名称\|学位名称\|开始时间\|结束时间 |
| `教育3` | String | Doctoral degree info | 大学名称\|专业名称\|学位名称\|开始时间\|结束时间 |
| `工作1-5` | String | Work history (up to 5) | 公司名称\|职位名称\|开始时间\|结束时间 |
| `certification` | String | Certificates and qualifications | 原文摘录 |
| `charity` | String | Charity activities | 原文摘录 |
| `prize` | String | Awards and recognitions | 原文摘录 |
| `hobby` | String | Personal hobbies | 原文摘录 |
| `expert_in` | String | Areas of expertise | 原文摘录 |
| `writings` | String | Publications and writings | 原文摘录 |
| `part-time_job` | String | Part-time positions | 原文摘录 |
| `social_activities` | String | Social activities | 原文摘录 |
| `OTHER` | String | Other unclassified information | 原文摘录 |

## Data Formatting Rules

### Date Format
- Use `yyyymm` format (e.g., `201901` for January 2019)
- If only year is available, use `01` for month
- Use `-` for missing dates

### Missing Information
- Use `-` for any missing or unavailable information
- Empty cells should be avoided

### Education History Priority
- 教育1: Bachelor's degree (学士学位)
- 教育2: Master's degree (硕士学位) 
- 教育3: Doctoral degree (博士学位)
- Functions/correspondence education counts as bachelor's degree

### Work History
- List in chronological order (most recent first recommended)
- Maximum 5 work experiences
- Include all relevant positions

## Example Data Entries

### Education History Example
```
香港理工大学|理学|硕士|201709|201906
```

### Work History Example
```
泰达宏利基金管理有限公司|市场总监|200408|200709
```

### Missing Information Example
```
香港理工大学|-|硕士|-|-
```

## Quality Guidelines

1. **Completeness**: Ensure all available information is captured
2. **Accuracy**: Verify dates and names are correctly formatted
3. **Consistency**: Use consistent formatting across all records
4. **Validation**: Check that processed data makes logical sense

## Common Issues

1. **Date Parsing**: Some resumes may have inconsistent date formats
2. **Name Variations**: Company/school names may have multiple versions
3. **Missing Context**: Some information may be ambiguous without context
4. **Character Encoding**: Ensure proper Chinese character handling

