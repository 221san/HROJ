import json 
# import markdown
import os

class config:
    hroj_prob = "./hroj.db/hroj_prob.json"
    
    pl = {}
    pl['C++ 17'] ="cpp"    

def get_problems():
    return json.loads( open(config.hroj_prob,"r").read())

def problem_info(problem_id):
    db = get_problems()
    
    for problemname,info in db.items():
        if(problemname==problem_id):
            return info
        
    return "!"

def language_compiler_version(language):
    return config.pl[language]
    

# def markdown_statement(statement):
#     html = markdown.markdown(statement)
#     return html