import cirq
import qsimcirq
import time
from cirq.contrib.qasm_import import circuit_from_qasm
import sys

time_start=time.time()

qasm_file = sys.argv[1]
with open(qasm_file, 'r') as qasm:
  data = qasm.read()
  circuit = circuit_from_qasm(data)
  qsimSim = qsimcirq.QSimSimulator()
  time_start=time.time()
  result = qsimSim.run(circuit)
  time_end=time.time()
  print('time cost',time_end-time_start,'s')

    
