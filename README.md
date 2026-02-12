

# PerioDx-Tx Net: Multimodal Transformer for Periodontal Disease Diagnosis

This repository contains the dataset construction guidelines, data preprocessing details, and training scripts for **PerioDx-Tx Net**. This system is designed to automate periodontal disease diagnosis (Staging & Grading) and detect superimposed lesions using the **Qwen2-VL** vision-language model architecture.

## 1. Dataset Overview

The dataset is constructed from real-world clinical data collected from multiple centers, including the West China Hospital of Stomatology.

* **Total Sample Size**: 2,016 patient cases.
* **Data Modality**: Panoramic Radiographs (Images) + Diagnostic Labels/Context (Text).
* **Data Splitting**: Patient-level random splitting.
* **Training Set**: 60%
* **Validation Set**: 10%
* **Test Set**: 30%



## 2. Data Construction & Preprocessing

To handle clinical complexity, we constructed two specific classification tasks. The data preprocessing pipeline ensures class balance and rigorous negative sampling.

### Task 1: Periodontal Staging vs. Health

**Objective**: Classify the patient's condition into one of 5 categories based on the radiographic image.

* **Prompt Template**:
> "请结合提供的口腔图像，判断当前口腔状况是否存在慢性牙周炎？仅从[慢性牙周炎1期、慢性牙周炎2期、慢性牙周炎3期、慢性牙周炎4期、健康]中选取1个符合的答案。"


* **Labels**: `Health`, `Stage I`, `Stage II`, `Stage III`, `Stage IV`.
* **Balancing Strategy**:
* 
**Oversampling**: For categories with fewer samples, data is duplicated to ensure each category accounts for at least **15%** of the total training data.





### Task 2: Superimposed Lesion Judgment

**Objective**: Given a *known* periodontal stage, determine if a superimposed lesion exists.

* **Prompt Template**:
> "已知结合口腔CT图像判断当前存在[insert_stage_here]，请进一步分析该慢性牙周炎是否叠加了其他口腔病变？仅从[牙龈瘤、牙龈炎、牙周牙髓联合病变、无叠加病变]中选取1个符合的答案。"


* **Labels**: `Epulis` (牙龈瘤), `Gingivitis` (牙龈炎), `Periodontal-Endodontic Lesion` (牙周牙髓联合病变), `No Superimposed Lesion` (无叠加病变).
* **Construction Logic**:
* **Positive Samples**: Cases with confirmed superimposed lesions.
* **Negative Sampling**: We randomly selected cases from Stage I-IV periodontitis that *do not* have superimposed lesions and explicitly labeled them as "No Superimposed Lesion" (无叠加病变).
* **Balancing**: Similar to Task 1, rare lesion types are oversampled to meet the 15% threshold.



---

## 3. Directory Structure

Please organize your data as follows to ensure compatibility with the training scripts:

```text
PerioDx-Tx-Net/
├── data/
│   ├── images/                     # Folder containing raw panoramic images
│   │   ├── patient_001.jpg
│   │   └── ...
│   ├── dataset_train.json          # Constructed training data (60%)
│   ├── dataset_val.json            # Constructed validation data (10%)
│   └── dataset_test.json           # Constructed test data (30%)
├── scripts/
│   └── sft_medicine_lora.sh        # Fine-tuning shell script
└── README.md                       # Project documentation

```

---

## 4. Data Format (JSON)

The dataset uses the standard format required for **Qwen2-VL-Instruct** fine-tuning.

### Example: Task 1 (Staging)

```json
{
  "id": "train_001",
  "image": ["data/images/patient_001.jpg"],
  "conversations": [
    {
      "role": "user",
      "content": "Picture 1: <img>data/images/patient_001.jpg</img>\n请结合提供的口腔图像，判断当前口腔状况是否存在慢性牙周炎？仅从[慢性牙周炎1期、慢性牙周炎2期、慢性牙周炎3期、慢性牙周炎4期、健康]中选取1个符合的答案。"
    },
    {
      "role": "assistant",
      "content": "慢性牙周炎3期"
    }
  ]
}

```

### Example: Task 2 (Superimposed Lesion)

```json
{
  "id": "train_002",
  "image": ["data/images/patient_002.jpg"],
  "conversations": [
    {
      "role": "user",
      "content": "Picture 1: <img>data/images/patient_002.jpg</img>\n已知结合口腔CT图像判断当前存在[慢性牙周炎4期]，请进一步分析该慢性牙周炎是否叠加了其他口腔病变？仅从[牙龈瘤、牙龈炎、牙周牙髓联合病变、无叠加病变]中选取1个符合的答案。"
    },
    {
      "role": "assistant",
      "content": "牙周牙髓联合病变"
    }
  ]
}

```

---

## 5. Training

We provide a shell script `scripts/sft_medicine_lora.sh` to fine-tune the model using **LoRA** (Low-Rank Adaptation).

### Requirements

* Python 3.8+
* PyTorch
* Transformers (Hugging Face)
* Qwen2-VL dependencies

### Usage

Run the following command from the root directory:

```bash
sh scripts/sft_medicine_lora.sh

```

### Script Arguments

The script is pre-configured with the following key parameters:

* 
`--model_name_or_path`: `Qwen/Qwen2-VL-2B-Instruct` 


* `--data_path`: Path to your JSON dataset (e.g., `data/dataset_train.json`).
* `--use_lora`: `true` (Uses parameter-efficient fine-tuning).
* `--bf16`: `true` (Uses BFloat16 precision for training stability).
* `--output_dir`: Checkpoints will be saved to `output_medicine_lora`.

