from datetime import datetime
import os
import cnf_builder
import argparse
import time

def call_kissat(cnf_file, out_put_path, time_out):
    os.system("./kissat/build/kissat {} --time={} > {}".format(cnf_file, str(time_out), out_put_path))

def get_name_of_encoding_mode(mode):
    return {1: "binomial", 2: "new_sequential_counter", 3: "old_sequential_counter"}.get(mode, "Invalid")

def process(database, min_support, mode, time_out):
    encoding_mode_name = get_name_of_encoding_mode(mode)
    if (encoding_mode_name == "Invalid"):
        print("Invalid encoding mode.")
        return
    
    cnf_folder_path = "cnf/{}".format(encoding_mode_name)
    output_folder_path = "output/{}".format(encoding_mode_name)
    
    file_prefix = str(datetime.now()).replace(" ", "_")
    file_name = "{}__{}".format(file_prefix, database.split('/')[-1])
    
    cnf_file_path = "{}/{}".format(cnf_folder_path, file_name)
    output_file_path = "{}/{}".format(output_folder_path, file_name)
    
    start_time = time.time()
    n_items, n_transactions, n_vars, n_clauses = cnf_builder.run(database, cnf_file_path, min_support, mode)
    call_kissat(cnf_file_path, output_file_path, time_out)
    elapsed_time = time.time() - start_time
    return n_items, n_transactions, n_vars, n_clauses, elapsed_time

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--database', '-db', type=str, required=True, dest='database', help='Path to the input database')
    parser.add_argument('--min-support', '-msup', required=True, dest='min_support', type=float, help='Minimum support of itemset. Minimum value in range (0, 1) is counted as percentage .i.e 0.7 <=> 70%%, while [1, ...] is counted as number of transactions')
    parser.add_argument('--mode', type=int, default=1, required=True, dest='mode', choices=[1, 2, 3], help='Encoding mode:    1. Binomial    2. New sequential Counter    3. Old sequential Counter')
    parser.add_argument('--time-out', type=int, default=900, required=False, dest='time_out', help='Timeout for SAT solver')
    args = parser.parse_args()
    (n_items, n_transactions, n_vars, n_clauses, elapsed_time) = process(args.database, args.min_support, args.mode, args.time_out)
    print("Report:\n\tItems: {}\n\tTransactions: {}\n\tVariables: {}\n\tClauses: {}\n\tElapse time:{}"
          .format(n_items, n_transactions, n_vars, n_clauses, elapsed_time))