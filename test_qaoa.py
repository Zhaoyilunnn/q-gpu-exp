# QAOA example
import numpy as np
import networkx as nx
import sys
import json
import time
from qiskit import BasicAer
from qiskit import Aer
from qiskit.aqua.algorithms import NumPyMinimumEigensolver
from qiskit.optimization.applications.ising import graph_partition
from qiskit.optimization.applications.ising.common import random_graph, sample_most_likely
from qiskit.aqua import aqua_globals
from qiskit.aqua.algorithms import QAOA
from qiskit.aqua.components.optimizers import COBYLA
from qiskit.circuit.library import TwoLocal
from qiskit.compiler import transpile, assemble

if len(sys.argv) != 3:
    print("Usage: %s <num-qubits> <method>" % sys.argv[0])
    sys.exit(1)


num_nodes = int(sys.argv[1])
method = sys.argv[2]  # statevector_gpu or statevector
w = random_graph(num_nodes, edge_prob=0.8, weight_range=10, seed=48)

G = nx.from_numpy_matrix(w)
layout = nx.random_layout(G, seed=10)
# colors = ['r', 'g', 'b', 'y']
# nx.draw(G, layout, node_color=colors)
# labels = nx.get_edge_attributes(G, 'weight')
# nx.draw_networkx_edge_labels(G, pos=layout, edge_labels=labels)


def brute_force():
    # use the brute-force way to generate the oracle
    def bitfield(n, L):
        result = np.binary_repr(n, L)
        return [int(digit) for digit in result]  # [2:] to chop off the "0b" part

    L = num_nodes
    max = 2**L
    minimal_v = np.inf
    for i in range(max):
        cur = bitfield(i, L)

        how_many_nonzero = np.count_nonzero(cur)
        if how_many_nonzero * 2 != L:  # not balanced
            continue

        cur_v = graph_partition.objective_value(np.array(cur), w)
        if cur_v < minimal_v:
            minimal_v = cur_v
    return minimal_v

qubit_op, offset = graph_partition.get_operator(w)
print("Number of Qubits: %s" % qubit_op.num_qubits)

aqua_globals.random_seed = 10598
optimizer = COBYLA(maxiter=1, tol=1e3)
backend = Aer.get_backend('qasm_simulator')
backend.set_options(method=method)
backend.set_options(max_memory_mb=307200)
#backend.set_options(fusion_enable=False) # TODO: Make this an option
qaoa = QAOA(qubit_op, optimizer, quantum_instance=backend)
#circ = qaoa.construct_circuit([0.0, 0.0])
#qobject = assemble(circ)
#qobject.to_dict()
#with open("qaoa.job", 'w') as f:
#    f.write(json.dumps(qobject.to_dict()))
#
#
#backend_options = {'method': 'statevector_gpu'}
#with open("qaoa.config", 'w') as f:
#    f.write(json.dumps(backend_options))

start = time.time()
result = qaoa.compute_minimum_eigenvalue()
end = time.time()

x = sample_most_likely(result.eigenstate)
ising_sol = graph_partition.get_graph_solution(x)

print(ising_sol)
print(f'Objective value computed by QAOA is {graph_partition.objective_value(x, w)}')
print("Execution time: %s" % (end - start))
