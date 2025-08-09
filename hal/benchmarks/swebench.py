        
        
        command = ['conda', 'run', '-n', 'swebench_hal', 'python', '-m', 'swebench.harness.run_evaluation',
           '--dataset_name', 'princeton-nlp/SWE-bench_Verified',
           '--predictions_path', submissions_path,
           '--max_workers', '6',
           '--run_id', run_id]

        # Ensure Docker Python SDK can connect to Docker Desktop on macOS by setting DOCKER_HOST
        env = os.environ.copy()
        if not os.path.exists('/var/run/docker.sock'):
            user_sock = os.path.expanduser('~/.docker/run/docker.sock')
            if os.path.exists(user_sock):
                env['DOCKER_HOST'] = f'unix://{user_sock}'
        
        try:
            subprocess.run(['conda', 'create', '-n', 'swebench_hal', 'python=3.11', '-y', '--force'], check=True, env=env)
            subprocess.run([
                'conda', 'run', 
                '-n', 'swebench_hal', 
                'pip', 'install', 
                '-e', 'git+https://github.com/benediktstroebl/SWE-bench.git#egg=swebench'], check=True, env=env)

            subprocess.run(command, check=True, env=env)
            
            # Load the evaluation results
            with open(f"{self.benchmark_name}.{run_id}.json", 'r') as f:
                results = json.load(f)

            # delete file
            os.remove(f"{self.benchmark_name}.{run_id}.json")
            
            # remove conda environment
            # subprocess.run(['conda', 'env', 'remove', '-n', 'swebench_hal', '--yes', '--all'], check=True)

            return results


        except subprocess.CalledProcessError as e:
            print(f"Error running SWE-bench evaluation harness: {e}")
            print(f"Stdout: {e.output}")
            print(f"Stderr: {e.stderr}")
            raise