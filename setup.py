import os 
import argparse
import subprocess


parser = argparse.ArgumentParser()
parser.add_argument('-pyv', type=str, required=False, help='python version por example python, python3 or py',default = 'python3')


args = parser.parse_args()


def run_setup( python_v:str ) -> None:
    print(
    ''' 


        | |   (_) |            / _|
        | |__  _| | _____  ___| |_ ___  _ __ _____   _____ _ __ 
        | '_ \| | |/ / _ \/ __|  _/ _ \| '__/ _ \ \ / / _ \ '__|
        | |_) | |   <  __/\__ \ || (_) | | |  __/\ V /  __/ |   
        |_.__/|_|_|\_\___||___/_| \___/|_|  \___| \_/ \___|_|  



    '''
)
  

    # run etl process
    os.chdir('./src')  
    os.system(f'{python_v} main.py')
    
    # run api server
    os.chdir('../api')
    subprocess.Popen([f'{python_v}','apiMain.py'])
    
    # run streamlit  
    os.chdir('../front')
    os.system(f'streamlit run home.py')


if __name__ == '__main__':
   run_setup(args.pyv)



