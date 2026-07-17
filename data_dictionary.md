# Data Dictionary - Gen Z Payment Analysis

## Survey Data Structure

### Demographics Section

| Field Name | Data Type | Description | Values |
|-----------|-----------|-------------|--------|
| `respondent_id` | String (UUID) | Unique respondent identifier | Auto-generated |
| `generation` | Categorical | Generational cohort | Gen Z, Alpha Gen Z, Millennial, Gen X, Boomer |
| `age` | Integer | Age in years | 8-85 |
| `age_group` | Categorical | Age grouped in bins | 8-13, 14-18, 19-25, 26-29, 30-45, 46-61, 62+ |
| `gender` | Categorical | Gender identity | Male, Female, Non-binary, Prefer to specify, Prefer not to say |
| `location` | String | State/Region | US state abbreviations |
| `country` | Categorical | Country of residence | United States, Canada, Other |
| `employment_status` | Categorical | Current employment | Student, Full-time, Part-time, Self-employed, Unemployed, Retired |
| `annual_household_income` | Categorical | Income bracket | <$25k, $25-50k, $50-75k, $75-100k, $100-150k, $150k+ |
| `education_level` | Categorical | Highest education achieved | High School, Some College, Bachelor's, Master's, PhD |
| `device_primary` | Categorical | Primary device used | Smartphone, Tablet, Laptop, Desktop |
| `banking_app_frequency` | Categorical | Banking app usage | Daily, Several times/week, Weekly, Monthly, Rarely, Never |

### Payment Method Usage Section

**For each payment method, collect:**

| Field Name Pattern | Data Type | Description | Example |
|------------------|-----------|-------------|---------|
| `{method}_usage` | Categorical | Usage status | Active User, Aware Non-User, Unaware |
| `{method}_frequency` | Categorical | Usage frequency | Daily, Weekly, Monthly, Rarely |
| `{method}_purchase_pct` | Integer | % of purchases with this method | 0-100 |
| `{method}_satisfaction` | Integer | Satisfaction rating | 1-5 scale |

**Payment Methods:**
- `digital_wallet` - Apple Pay, Google Pay, Samsung Pay
- `bnpl` - Buy Now Pay Later services
- `credit_card` - Physical and digital credit cards
- `debit_card` - Physical and digital debit cards
- `paypal_venmo` - PayPal and similar services
- `cryptocurrency` - Bitcoin, Ethereum, stablecoins
- `bank_transfer` - Direct bank transfers, ACH
- `mobile_banking_app` - Direct app-based payments

### Primary Payment Method

| Field Name | Data Type | Description | Values |
|-----------|-----------|-------------|--------|
| `primary_payment_method` | Categorical | Most used payment method | [Payment methods listed above] |
| `primary_method_reason` | Text | Why this is primary method | Free-form text response |
| `secondary_payment_method` | Categorical | Second most used method | [Payment methods listed above] |
| `switch_likelihood` | Integer | Likelihood to switch methods | 1-5 scale |
| `switch_reason` | Text | Reason for potential switch | Free-form text |

### Feature Importance Ratings

All rated on 1-5 scale (1=Not Important, 5=Critical):

| Field Name | Description |
|-----------|-------------|
| `speed_importance` | Transaction speed and quick checkout |
| `security_importance` | Security and fraud protection |
| `privacy_importance` | Data privacy and protection |
| `ease_of_use_importance` | Ease of use and simplicity |
| `rewards_importance` | Rewards, cashback, points |
| `mobility_importance` | Mobile compatibility and accessibility |
| `biometric_importance` | Biometric authentication (fingerprint, face) |
| `sustainability_importance` | Environmental/ethical impact |
| `fee_transparency_importance` | Clear and transparent fees |
| `recurring_importance` | Ability to set up recurring payments |

### Digital Wallets & BNPL Section

| Field Name | Data Type | Description | Values |
|-----------|-----------|-------------|--------|
| `digital_wallet_awareness` | Categorical | Awareness of digital wallets | Yes, No, Vague |
| `digital_wallet_adoption` | Categorical | Usage of digital wallets | Active User, Aware Non-User, Unaware |
| `digital_wallet_frequency` | Categorical | How often used | Never to Multiple times daily |
| `digital_wallet_satisfaction` | Integer | Satisfaction rating | 1-5 scale |
| `digital_wallet_barriers` | Text (multiple) | Reasons not using if applicable | Checkbox list |
| `bnpl_awareness` | Categorical | Awareness of BNPL services | Yes, No, Vague |
| `bnpl_adoption` | Categorical | Usage of BNPL | Active User, Aware Non-User, Unaware |
| `bnpl_frequency` | Categorical | How often used BNPL | Never to Multiple times per month |
| `bnpl_provider` | Categorical | Preferred BNPL provider | Klarna, Afterpay, Affirm, Other |
| `bnpl_satisfaction` | Integer | Satisfaction with BNPL | 1-5 scale |
| `bnpl_concerns` | Text (multiple) | Concerns about BNPL | Checkbox list (debt, fees, complexity, etc.) |

### Security & Privacy Section

| Field Name | Data Type | Description | Values |
|-----------|-----------|-------------|--------|
| `privacy_concern_level` | Integer | How concerned about privacy | 1-5 scale |
| `provider_trust_level` | Integer | Trust in payment providers | 1-5 scale |
| `biometric_interest` | Categorical | Interest in biometric auth | Yes, No, Not sure |
| `acceptable_data_sharing` | Categorical | Comfortable data sharing level | None, Minimum, Some, All |
| `fraud_experience` | Categorical | Ever experienced payment fraud | Yes, No, Not sure |
| `security_concern_level` | Integer | General security concerns | 1-5 scale |
| `preferred_auth_method` | Categorical | Preferred authentication | Password, Biometric, 2FA, Other |
| `new_security_adoption` | Integer | Would adopt if more secure | 1-5 scale likelihood |

### Emerging Technologies Section

| Field Name | Data Type | Description | Values |
|-----------|-----------|-------------|--------|
| `crypto_awareness` | Categorical | Cryptocurrency awareness | Yes, No, Vague |
| `crypto_interest` | Integer | Interest in crypto payments | 1-5 scale |
| `blockchain_knowledge` | Categorical | Blockchain understanding | None, Basic, Good, Expert |
| `decentralized_payments_interest` | Integer | Interest in decentralized payments | 1-5 scale |
| `ai_payment_interest` | Integer | Interest in AI-powered payments | 1-5 scale |
| `emerging_tech_interest` | Text | Most interesting emerging payment method | Free-form |
| `emerging_adoption_likelihood` | Integer | Likelihood to adopt emerging methods | 1-5 scale |
| `emerging_tech_concerns` | Text (multiple) | Concerns about new technologies | Checkbox/text |

### Future Outlook Section

| Field Name | Data Type | Description | Values |
|-----------|-----------|-------------|--------|
| `future_primary_method_5yr` | Categorical | Expected primary method in 5 years | [Payment methods] |
| `future_preference_change` | Text | How preferences will change | Free-form |
| `future_feature_desires` | Text (multiple) | Desired new features | Checkbox/text |
| `environmental_influence` | Categorical | Environmental impact influences choice | Yes, No, Somewhat |
| `premium_for_sustainability` | Categorical | Willing to pay premium for eco-friendly | Yes, No, Maybe |
| `additional_feedback` | Text | Any final thoughts | Open-ended text |

### Metadata

| Field Name | Data Type | Description |
|-----------|-----------|-------------|
| `response_date` | DateTime | Date/time survey completed |
| `completion_time` | Integer | Time to complete in seconds |
| `device_type` | Categorical | Device survey taken on | Mobile, Tablet, Desktop |
| `ip_address_masked` | String | Masked IP for deduplication | Last octet masked for privacy |
| `data_quality_flag` | Categorical | Data quality assessment | Good, Fair, Poor |

---

## Data Coding Guidelines

### Missing Data Codes
- **Blank/NULL** - Skipped or did not respond
- **-1** - Not applicable to respondent
- **-2** - Refused to answer
- **-3** - Don't know/Unsure

### Categorical Value Standardization
All values should be:
- Title case for consistency
- No leading/trailing spaces
- Consistent across all responses
- Documented in this dictionary

### Text Response Handling
- Free-form text responses should be stored as-is
- Clean of special characters unless necessary
- Note any redacted PII (removed in processing)
- Store original response in raw data

### Data Quality Checks
- Response time: Flag if <3 min or >30 min
- Logical consistency: Age matches generation
- Pattern checking: Extreme/unusual responses
- Completeness: Required fields present
- Duplicates: Same respondent multiple times

---

## Data Processing Steps

### 1. Raw Data Ingestion
- Import from survey platform
- Verify column names match this dictionary
- Check for encoding issues
- Document any data collection issues

### 2. Data Cleaning
- Remove test/pilot responses
- Delete duplicate respondents
- Handle missing values
- Standardize categorical values
- Parse dates to datetime objects

### 3. Data Validation
- Age validation (8-85 reasonable range)
- Generation auto-calculation from age
- Logical consistency checks
- Outlier identification

### 4. Data Enrichment
- Calculate age groups from age
- Calculate adoption rates
- Derive segments/clusters
- Calculate satisfaction averages

### 5. Data Anonymization
- Remove PII (names, contact info)
- Mask IP addresses
- Remove any identifying text
- Aggregate to level that prevents identification

---

## Analysis Variables Created

### Derived Variables

| Variable Name | Derivation | Purpose |
|--------------|-----------|---------|
| `digital_wallet_score` | Adoption + Frequency + Satisfaction | Overall digital wallet health |
| `bnpl_adoption_stage` | Awareness → Consideration → Adoption | BNPL funnel stage |
| `feature_priority_index` | Top 3 features average | Feature importance ranking |
| `payment_method_diversity` | Count of methods used | Payment portfolio diversity |
| `security_consciousness` | Privacy + Security + Auth method scores | Security orientation |

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | July 2026 | Initial data dictionary |
| 1.1 | [TBD] | Updates based on pilot survey |

---

**Last Updated:** July 2026  
**Data Dictionary Version:** 1.0  
**Status:** Ready for Use

