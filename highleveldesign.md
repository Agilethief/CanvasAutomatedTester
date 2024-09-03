# High level design

## Main Objects:

### Course - course wide information

- ID : int
- Title : string
- Participant count : int
- Page count : int
- Assessment count : int
- link count : int
- Image count : int

### Module - Module info

- Title : string
- Page count : int
- Assessment count : int

### Page - Page information

- URL : int
- Title : string
- Module : string
- link count : int
- Image count : int
- Word Count : int

### Assessment - Info

- URL : int
- Title : string
- Module : string
- link count : int
- Image count : int
- Word Count : int

Report - contains the findings of a series of tests

---

## Flow

1. Script starts
2. Log into Canvas - https://wisdomlearning.instructure.com/login/canvas
3. Get starting ID (650)
4. Navigate to first course to check - https://wisdomlearning.instructure.com/courses/{ID}/
   1. Confirm valid course
   2. Run Tests on course
   3. Generate Report based on tests
   4. Save and share report
5. Increment ID
