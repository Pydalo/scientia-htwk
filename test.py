import transformers
print(transformers.__version__)
print(transformers.__file__)

from transformers import TrainingArguments
import inspect

print(inspect.signature(TrainingArguments))