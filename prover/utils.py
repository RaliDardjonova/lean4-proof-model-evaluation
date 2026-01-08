import os
import sys
import json
import pytz
from pathlib import Path
from datetime import datetime
from collections import UserDict
from importlib.machinery import SourceFileLoader
from easydict import EasyDict as AttrDict


LEAN4_DEFAULT_HEADER = "import Mathlib\nimport Aesop\n\nset_option maxHeartbeats 0\n\nopen BigOperators Real Nat Topology Rat\n\n"

def non_cot_prompt(data):
    return "Complete the following Lean 4 code:\n\n```lean4\n{header}{informal_prefix}{formal_statement}".format(
        header=data.get('header', LEAN4_DEFAULT_HEADER),
        informal_prefix=data.get('informal_prefix', str()),
        formal_statement=data['formal_statement'],
    )

def non_cot_few_shot_prompt(data):
    return "Complete the following Lean 4 code:\n\n```lean4\n{header}{informal_prefix}{formal_statement}{formal_proof}\n```\n\n\n".format(
        header=data.get('header', LEAN4_DEFAULT_HEADER),
        informal_prefix=data.get('informal_prefix', str()),
        formal_statement=data['formal_statement'],
        formal_proof=data['formal_proof'],
    )

def cot_prompt(data):
    return "Complete the following Lean 4 code with explanatory comments preceding each line of code:\n\n```lean4\n{header}{informal_prefix}{formal_statement}".format(
        header=data.get('header', LEAN4_DEFAULT_HEADER),
        informal_prefix=data.get('informal_prefix', str()),
        formal_statement=data['formal_statement'],
    )

def cot_few_shot_prompt(data):
    return "Complete the following Lean 4 code with explanatory comments preceding each line of code:\n\n```lean4\n{header}{informal_prefix}{formal_statement}{formal_proof}\n```\n\n\n".format(
        header=data.get('header', LEAN4_DEFAULT_HEADER),
        informal_prefix=data.get('informal_prefix', str()),
        formal_statement=data['formal_statement'],
        formal_proof=data['formal_proof'],
    )

def post_process_output(output):
    print(f'===============\n{output}\n==============\n', file=sys.stderr)

    _find_idx = output.find("```")
    return output[:_find_idx] if _find_idx >= 0 else output

def dsv2_prompt(data):
    input_prompt = "Complete the following Lean 4 code:\n\n```lean4\n{header}{informal_prefix}{formal_statement}```\n\n Before producing the Lean 4 code to formally prove the given theorem, provide a detailed proof plan outlining the main proof steps and strategies. The plan should highlight key ideas, intermediate lemmas, and proof structures that will guide the construction of the final formal proof.".format(
        header=data.get('header', LEAN4_DEFAULT_HEADER),
        informal_prefix=data.get('informal_prefix', str()),
        formal_statement=data['formal_statement'].split(":= by")[0] + " := by sorry",
    )
    print(f'Length input for {data["name"]}: {len(input_prompt)}', file=sys.stderr)

     
    return "Complete the following Lean 4 code:\n\n```lean4\n{header}{informal_prefix}{formal_statement}```\n\n Before producing the Lean 4 code to formally prove the given theorem, provide a detailed proof plan outlining the main proof steps and strategies. The plan should highlight key ideas, intermediate lemmas, and proof structures that will guide the construction of the final formal proof.".format(
        header=data.get('header', LEAN4_DEFAULT_HEADER),
        informal_prefix=data.get('informal_prefix', str()),
        formal_statement=data['formal_statement'].split(":= by")[0] + " := by sorry",
    )

def dsv2_inline_cot_prompt(data):
    return "Complete the following Lean 4 code:\n\n```lean4\n{header}{informal_prefix}{formal_statement}```\n\n Before producing the Lean 4 code to formally prove the given theorem, provide a detailed proof plan outlining the main proof steps and strategies. The plan should highlight key ideas, intermediate lemmas, and proof structures that will guide the construction of the final formal proof. You can use maximum 512 tokens for thinking and planing.".format(
        header=data.get('header', LEAN4_DEFAULT_HEADER),
        informal_prefix=data.get('informal_prefix', str()),
        formal_statement=data['formal_statement'].split(":= by")[0] + " := by sorry",
    )

    
def dsv2_few_shot_prompt(data):
    return "Complete the following Lean 4 code:\n\n```lean4\n{header}{informal_prefix}{formal_statement}{formal_proof}\n```\n\n\nBefore producing the Lean 4 code to formally prove the given theorem, provide a detailed proof plan outlining the main proof steps and strategies. The plan should highlight key ideas, intermediate lemmas, and proof structures that will guide the construction of the final formal proof.".format(
        header=data.get('header', LEAN4_DEFAULT_HEADER),
        formal_statement=data['formal_statement'],
        informal_prefix=data.get('informal_prefix', str()),
        formal_proof=data['formal_statement'].split(":= by")[0] + " := by sorry",
    )

def goedel_prompt(data):
    return "Complete the following Lean 4 code:\n\n```lean4\n{header}{formal_statement}```\n\n Before producing the Lean 4 code to formally prove the given theorem, provide a detailed proof plan outlining the main proof steps and strategies. The plan should highlight key ideas, intermediate lemmas, and proof structures that will guide the construction of the final formal proof.".format(
        header=data.get('header', LEAN4_DEFAULT_HEADER),
        formal_statement=data['formal_statement'].split(":= by")[0] + " := by sorry",
    )


def goedel_non_cot_prompt(data):
    return "Complete the following Lean 4 code:\n\n```lean4\n{header}{formal_statement}```\n\n Generate only the Lean 4 code for the following theorem. Do not provide natural language explanations or thoughts.".format(
        header=data.get('header', LEAN4_DEFAULT_HEADER),
        formal_statement=data['formal_statement'].split(":= by")[0] + " := by sorry",
    )


    
def goedel_few_shot_prompt(data):
    return "Complete the following Lean 4 code:\n\n```lean4\n{header}{formal_statement}{formal_proof}\n```\n\n\nBefore producing the Lean 4 code to formally prove the given theorem, provide a detailed proof plan outlining the main proof steps and strategies. The plan should highlight key ideas, intermediate lemmas, and proof structures that will guide the construction of the final formal proof.".format(
        header=data.get('header', LEAN4_DEFAULT_HEADER),
        formal_statement=data['formal_statement'],
        formal_proof=data['formal_statement'].split(":= by")[0] + " := by sorry",
    )

def kimina_prompt(data):
    return "Think about and solve the following problem step by step in Lean 4.\n# Problem:{informal_prefix}\n# Formal statement:\n```lean4\n {header}{informal_prefix}{formal_statement}\n```\n".format(
        header=data.get('header', LEAN4_DEFAULT_HEADER),
        informal_prefix=data.get('informal_prefix', str()),
        formal_statement=data['formal_statement'],
    )

def kimina_few_shot_prompt(data):
    return "Think about and solve the following problem step by step in Lean 4.\n# Problem:{informal_prefix}\n# Formal statement:\n```lean4\n {header}{informal_prefix}{formal_statement}\n```\n{formal_proof}\n```\n\n\n".format(
        header=data.get('header', LEAN4_DEFAULT_HEADER),
        informal_prefix=data.get('informal_prefix', str()),
        formal_statement=data['formal_statement'],
        formal_proof=data['formal_proof'],
    )

def post_process_output_test(output):
    spl = output.split("```lean4")
    if len(spl) <= 1:
        result =  output
    if not spl[-1].strip():
        result = spl[-2].split('```')[0]
    else:    
        result = spl[-1].split('```')[0]
    
    print(f'+++++++++++++++\n{output}\n++++++++++++++\n', file=sys.stderr)
    print(f'===============\n{result}\n==============\n', file=sys.stderr)
    #print(f'Length output: {len(output)}', file=sys.stderr)
    return result
    # _find_idx = output.find("```")
    # print('Index found: ', _find_idx, file=sys.stderr)
    # print(f'===============\n{output}\n==============\n', file=sys.stderr)
    # return output[_find_idx:] if _find_idx >= 0 else output


    
MODEL_FORMAT = dict(
    non_cot=dict(prompt=non_cot_prompt, output=post_process_output, few_shot=non_cot_few_shot_prompt),
    cot=dict(prompt=cot_prompt, output=post_process_output, few_shot=cot_few_shot_prompt),
    goedel=dict(prompt=goedel_prompt, output=post_process_output_test, few_shot=goedel_few_shot_prompt),
    goedel_non_cot=dict(prompt=goedel_non_cot_prompt, output=post_process_output_test, few_shot=goedel_few_shot_prompt),
    kimina=dict(prompt=kimina_prompt, output=post_process_output, few_shot=kimina_few_shot_prompt),
    dsv2=dict(prompt=dsv2_prompt, output=post_process_output_test, few_shot=dsv2_few_shot_prompt),
    dsv2_inline=dict(prompt=dsv2_inline_cot_prompt, output=post_process_output_test, few_shot=cot_few_shot_prompt),
    dsv2_non_cot=dict(prompt=non_cot_prompt, output=post_process_output_test, few_shot=non_cot_few_shot_prompt),
    )


def get_datetime(readable=False):
    if readable:
        return datetime.now(pytz.timezone('Asia/Shanghai')).strftime("%Y/%m/%d %H:%M:%S")
    return datetime.now(pytz.timezone('Asia/Shanghai')).strftime("%Y%m%d_%H%M%S")

def load_config(fname):
    name = Path(fname).stem
    mod = SourceFileLoader(name, fname).load_module()

    config = {}
    for n in dir(mod):
        if not n.startswith("__"):
            config[n] = getattr(mod, n)
    config = AttrDict(config)

    return config

def load_jsonl_objects(input_path):
    objects = []
    with open(input_path, 'r', encoding='utf-8') as fr:
        for line in fr:
            objects.append(json.loads(line))
    return objects


class ConcurrentJob(object):
    def __init__(self, stage_list):
        assert len(stage_list) > 1
        self.stage_list = stage_list
        self.reset()
    
    def is_idle(self):
        return self._stage_idx is None
    
    def reset(self):
        self._stage_idx = None
        self._stage_cache = None
    
    def start(self, **kwargs):
        self._stage_idx = 1
        self._stage_cache = self.stage_list[0](**kwargs)
    
    def get_status(self):
        assert not self.is_idle()
        while True:
            status = self.stage_list[self._stage_idx](**self._stage_cache)
            if status is None:
                return None
            self._stage_idx += 1
            if self._stage_idx == len(self.stage_list):
                self.reset()
                return status
            self._stage_cache = status
