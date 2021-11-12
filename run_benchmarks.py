import sys
import argparse
from benchmark.noise import NoiseSimulatorBenchmarkSuite


def parse_args():
    parser = argparse.ArgumentParser(description='Benchmarks from qiskit circuit library: '
                                                 'qft\t'
                                                 'graph_state\t'
                                                 'hidden_linear_function\t'
                                                 'quadratic_form\t'
                                                 'iqp\t'
                                                 'grover_search\t'
                                                 'random_circuit')
    parser.add_argument('--num-qubits', type=int, default=10, help='number of qubits')
    parser.add_argument('--app', type=str, help='benchmark name')
    parser.add_argument('--fusion', type=str, default='false', help='whether fusion is turned on')
    parser.add_argument('--fusion-bits', type=int, default=5, help='max fusion size')
    parser.add_argument('--runtime', type=str, default='statevector_gpu', help='backend device')
    parser.add_argument('--save-qasm', type=str, default='false', help='option to save qasm')
    parser.add_argument('--save-conf', type=str, default='false', help='save q object configuration for debug')
    parser.add_argument('--seed', type=int, default=100, help='random seed for generating random_circuit')
    return parser.parse_args()


def _main():
    args = parse_args()
    qubits = [args.num_qubits]
    fusion_bits = args.fusion_bits
    seed = args.seed

    fusion = False
    save_qasm = False
    save_conf = False
   
    assert args.fusion in ['true', 'false']
    assert args.save_qasm in ['true', 'false']
    assert args.save_conf in ['true', 'false']

    if args.fusion == 'true':
        fusion = True
    if args.save_qasm == 'true':
        save_qasm = True
    if args.save_conf == 'true':
        save_conf = True
    
    app = args.app
    apps = {
        app: 1
    }
    noise_model_names = ['ideal']
    runtime_names = [args.runtime]
    measures = ['sampling']
    measure_counts = [1000]

    sim = NoiseSimulatorBenchmarkSuite(apps=apps,
                                       qubits=qubits,
                                       noise_model_names=noise_model_names,
                                       runtime_names=runtime_names,
                                       measures=measures,
                                       measure_counts=measure_counts,
                                       fusion_bits=fusion_bits,
                                       fusion=fusion,
                                       save_qasm=save_qasm,
                                       save_conf=save_conf,
                                       seed=seed)
    sim.run_manual()


if __name__ == '__main__':
    _main()
