import json 
import os
import subprocess
from datetime import date

class config:
    hroj_submissions = "./hroj.db/submissions.json"
    hroj_prob = "./hroj.db/hroj_prob.json"
    hroj_user = "./hroj.db/hroj_user.json"
    
def getdb():
    return json.loads( open(config.hroj_user,"r").read())

def get_submissions():
    return json.loads( open(config.hroj_submissions,"r").read())

def get_problems():
    return json.loads( open(config.hroj_prob,"r").read())

def update_last_submission():
    db = get_submissions()
    
    db[str(db['last'])]={}
    db['last']+=1
    with open(config.hroj_submissions,"w") as f:
        f.write(json.dumps(db,indent=4))    
    
def update_submission_info(id,info):
    db = get_submissions()
    db[str(id)]=info
    with open(config.hroj_submissions,"w") as f:
        f.write(json.dumps(db,indent=4))
    
class compiler:
    @staticmethod
    def cpp(testcase_input, testcase_output, code, _tok):
        
        id = get_submissions()['last']
        update_last_submission()
        try: 
            submissions_dir = "./compile"
            
            submission_dir = os.path.join(submissions_dir, str(id))
            os.makedirs(submission_dir, exist_ok=True)
            
            cpp_file_path = os.path.join(submission_dir, f"{id}.cpp")
            with open(cpp_file_path, "w") as codefile:
                codefile.write(code)
            
            compiled_file = os.path.join(submission_dir, f"{id}.exe")
            compile_command = ["g++", cpp_file_path, "-o", compiled_file]
            subprocess.run(compile_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            results = []
            for testcase_id in range(len(testcase_input)):
                input_data = testcase_input[testcase_id]
                expected_output = testcase_output[testcase_id]
                
                run_command = [compiled_file]
                process = subprocess.Popen(run_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                stdout, stderr = process.communicate(input=input_data)
                
                if process.returncode == 0 and stdout.strip() == expected_output.strip():
                    results.append("Accepted")
                else:
                    results.append("Wrong Answer")
                    
                print(submission_dir)
                
                # os.system(f"rm -rf {submission_dir}")
        except:
            results = ['Runtime Error']*len(testcase_input)
        return id,results
            
            
def profile_submission(tok,problem_id,pinfo,final,sub_id,nowdate):
    db = getdb()
    if(final=="Accepted"):
        if problem_id not in db[tok]['accepted']:
            db[tok]['accepted'].append(problem_id)
    db[tok]['submissions'].append({
        "date":nowdate,
        "problem_id":problem_id,
        "problem_name":pinfo['name'],
        "final":final,
        "sub_id":sub_id
    })
    with open(config.hroj_user,"w") as f:
        f.write(json.dumps(db,indent=4))
    
def submit_problem(problem_id,code,language,_tok):
    pinfo = get_problems()[problem_id]
    nowdate = str(date.today())
    
    testcase_input = pinfo['input']
    testcase_output = pinfo['output']
    # print(testcase_input,testcase_output,language,_tok)
    if(language == "cpp"):
        id,res = (compiler.cpp(testcase_input,testcase_output,code,_tok))    
        res = [ [i+1,res[i]] for i in range(0,len(res))]
        
    info = {
        "problem_id" : problem_id,
        "result":res,
        "token" : _tok,
        "code" : code,
        'date':nowdate
    }
    update_submission_info(id, info)
    
    final = "Accepted"
    for v in res:
        tst,st = v
        print(tst,st)
        if(st!=final):
            final=v
            break
        
    if final == "Accepted":
        final = [len(res),"Accepted"]
    profile_submission(_tok, problem_id, pinfo, final, id , nowdate)
    return id