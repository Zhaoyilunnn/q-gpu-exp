# qc-experiment

``` bash
pip install timeout-decorator

python run_benchmarks.py -h
```
# run basic benchmarks

``` bash
python run_benchmarks.py --app <qft | iqp | graph_state | hidden_linear_function | quadratic_form> --num-qubits <number of qubits> --fusion <true | false> --runtime <statevector | statevector_gpu (default)>
```

# run random circuit

``` bash
python run_benchmarks.py --app <path-to-rqc-qasm-file> --fusion <true | false>
e.g. python run_benchmarks.py --app random_circ/circuit_n20_m14_s3_e0_pEFGH.qasm --fusion true
```

# run qaoa

``` bash
python test_qaoa.py <num-qubits> <statevector | statevector_gpu>
```

# run hchain
``` bash
python hchain_vqe_single_iteration.py <num-hydrogen> <cpu | gpu> <qasm | statevector>
e.g. python hchain_vqe_single_iteration.py 2 gpu qasm 
```

# hchain
| num_h | num_qubits |
| -- | -- |
| 10 | 18 |
| 12 | 22 |
| 14 | 26 |
| 16 | 30 |
| 18 | 34 |
