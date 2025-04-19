
---

### 📄 `project_description.md`

```markdown
# 📊 Project Description: CSV Signal Merger

This project was created to streamline the preprocessing and merging of electrophysiological or behavioral signal data collected from various subjects or sessions, typically saved in Excel spreadsheets.

The input files are structured with two sheets:

- **metadata**: Describes the relationship between ROI names and source channels.
- **Processed**: Contains actual signal data, where columns are labeled using ROI names.

The goal is to transform this raw data into clean, uniformly labeled `.csv` files, and then merge all of them into a master CSV for downstream analysis.

---

## 🎯 Objectives

- Standardize column naming using provided metadata
- Enable dynamic merging of multiple signal files
- Keep only one reference time column (`Time (s)`)
- Ensure that merged columns follow a logical, analysis-ready order
  - First `pre` condition columns
  - Then `post` condition columns

---

## 📈 Use Cases

- Behavioral neuroscience
- Electrophysiology recordings
- Experimental sessions with varying pre/post treatment conditions
- Large datasets across multiple flies, animals, or recording dates

---

## 🔮 Output

The final output is a single CSV file named dynamically based on the shared descriptors in the input filenames. Example:

