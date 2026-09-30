from pathlib import Path
from transformers import AutoTokenizer, AutoModel
import torch


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

OUTPUT_DIR = Path("minilm_onnx")
OUTPUT_DIR.mkdir(exist_ok=True)

print("Loading tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

print("Loading model...")
model = AutoModel.from_pretrained(MODEL_NAME)
model.eval()

text = "Python machine learning recruitment assistant"

inputs = tokenizer(
    text,
    return_tensors="pt",
    padding=True,
    truncation=True,
    max_length=128
)

print("Exporting model to ONNX...")

torch.onnx.export(
    model,
    (
        inputs["input_ids"],
        inputs["attention_mask"],
        inputs["token_type_ids"]
    ),
    OUTPUT_DIR / "minilm.onnx",
    input_names=[
        "input_ids",
        "attention_mask",
        "token_type_ids"
    ],
    output_names=["last_hidden_state"],
    dynamic_axes={
        "input_ids": {0: "batch", 1: "sequence"},
        "attention_mask": {0: "batch", 1: "sequence"},
        "token_type_ids": {0: "batch", 1: "sequence"},
        "last_hidden_state": {0: "batch", 1: "sequence"}
    },
    opset_version=17
)
opset_version=17
external_data=False

print("ONNX export completed!")
print(f"Model saved at: {OUTPUT_DIR / 'minilm.onnx'}")
