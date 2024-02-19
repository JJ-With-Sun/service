import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel
from transformers import GenerationConfig
from datasets import Dataset
import warnings
import re
import pandas as pd

warnings.filterwarnings('ignore')

base_model_name='davidkim205/komt-mistral-7b-v1'
peft_model_name = "/home/kic/yskids/inbound/inbound_model/checkpoints/komt-mistral-7b-v1_lora_sftt/checkpoint-180"

class Evaluator:
    def __init__(self):
        self.base_model = AutoModelForCausalLM.from_pretrained(base_model_name, device_map="cuda:0",torch_dtype=torch.float16)
        self.peft_model = PeftModel.from_pretrained(self.base_model, peft_model_name)
        self.tokenizer = AutoTokenizer.from_pretrained(peft_model_name)
        self.peft_model=self.peft_model.merge_and_unload()


    def inference(self,path):
        # path의 jsonl 파일 리스트
        answer_path = path + '/answer/answer.jsonl'
        intro_path = path + '/introduction/intro_sample.xlsx'
        answer = Dataset.from_json(answer_path)
        intro = pd.read_excel(intro_path)
        for j in range(len(answer['answer'])):
            result = []
            for _, r in intro[['문항 1','문항 2','문항 3']].iterrows():
                prompt= "[INPUT]" + answer['answer'][j] + '에 대하여 작성한 에세이의 점수를 매겨주세요' + "[INST]" + r[j] + "[/INST]"
                print(prompt)

                generation_config = GenerationConfig(
                        temperature=0.1,
                        # top_p=0.8,
                        # top_k=100,
                        max_new_tokens=256,
                        repetiton_penalty=1.2,
                        early_stopping=True,
                        do_sample=True,
                    )

                gened = self.peft_model.generate(
                        **self.tokenizer(
                            prompt,
                            return_tensors='pt',
                            return_token_type_ids=False
                        ).to('cuda'),
                        generation_config=generation_config,
                        pad_token_id=self.tokenizer.eos_token_id,
                        eos_token_id=self.tokenizer.eos_token_id,
                        #streamer=streamer,
                    )
                result_str = self.tokenizer.decode(gened[0])
                start_tag = f"[/INST]"
                start_index = result_str.find(start_tag)

                if start_index != -1:
                    a = result_str[start_index + len(start_tag):].strip()
                print(a)
                a = a.split('.')[0]+'.'+a.split('.')[1]
                a = a.replace(' 평가지표는 ', '')
                parts = re.split('(\d+)', a)
                parts = [x.split(',')[1] if ',' in x else x for x in parts]
                print(parts)
                result.append(parts)
            intro[f'answer {j}'] = result
        intro['total'] = intro.apply(lambda row : int(row['answer 0'][1]) + int(row['answer 1'][1]) + int(row['answer 2'][1]),axis=1)
        top_half_indices = intro['total'].nlargest(intro.shape[0] // 2).index
        intro['status'] = '불합격'
        intro.loc[top_half_indices, 'status'] = '합격'
        intro.to_excel(path + '/result/result.xlsx', index=False)
            
                
        return intro

if __name__ == "__main__":
    path = "/home/kic/yskids/service/data/SAMSUNG"
    model = Evaluator()
    result = model.inference(path)
    print(result)
