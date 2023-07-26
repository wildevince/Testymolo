import os


#@background(schedule=1)  # schedule the task to run every 1 seconds
async def wait_for_muscle_outfile(file_path:str, max_attempts=10):
    if not os.path.exists(file_path):
        wait_for_muscle_outfile(file_path, max_attempts-1)
        if(max_attempts < 0):
            return False
    else:
        print("task: file is ready : "+file_path)
        return True
    

def check_outfile_ready(outfile_path:str):
    try:
        open(outfile_path, 'r')
        return True
    except Exception as e:
        print(e)
        return False