import sys
import time
from qiskit.chemistry import FermionicOperator
from qiskit.chemistry.drivers import PySCFDriver, UnitsType
from qiskit.aqua.operators import Z2Symmetries
from qiskit import Aer
from qiskit.aqua import QuantumInstance
from qiskit.aqua.components.optimizers import SPSA,COBYLA
# Use PySCF, a classical computational chemistry software
# package, to compute the one-body and two-body integrals in
# molecular-orbital basis, necessary to form the Fermionic operator
if len(sys.argv) != 4:
    print("Usage: %s <num-h> <device> <simulator>" % sys.argv[0])
    sys.exit(1)
num_h = int(sys.argv[1])
device = sys.argv[2]
runtime = sys.argv[3]
backend = Aer.get_backend("%s_simulator" % runtime)
backend.set_options(max_memory_mb=307200)
if device == "gpu":
    backend.set_options(method='statevector_gpu')
elif device == "cpu":
    backend.set_options(method='statevector')
else:
    raise ValueError("Invalid device")
    sys.exit(1)
seed=666
qi = QuantumInstance(backend=backend, seed_simulator=seed, seed_transpiler=seed, shots=1, measurement_error_mitigation_cls=None, noise_model=None)
assert (num_h % 2) == 0
def hydrogen_chain(num_h):
        atom_list = ""
        for i in range(num_h):
            if i > 0:
                atom_list += "; "
            atom_list += "H {:10.8f} {:10.8f} {:10.8f}".format(0.0, 0.0, 0.0 + (10.0 * i))
        nbeta = num_h // 2
        nalpha = num_h -nbeta
        spin = nalpha - nbeta
        return atom_list, spin
atoms = hydrogen_chain(num_h)[0]
driver = PySCFDriver(atom=atoms,
                     unit=UnitsType.ANGSTROM,
                     basis='sto3g')
molecule = driver.run()
num_particles = molecule.num_alpha + molecule.num_beta
num_spin_orbitals = molecule.num_orbitals * 2
# Build the qubit operator, which is the input to the VQE algorithm in Aqua
ferm_op = FermionicOperator(h1=molecule.one_body_integrals, h2=molecule.two_body_integrals)
map_type = 'PARITY'
qubit_op = ferm_op.mapping(map_type)
qubit_op = Z2Symmetries.two_qubit_reduction(qubit_op, num_particles)
num_qubits = qubit_op.num_qubits
print("Num qubits: %s" % num_qubits)
# setup a classical optimizer for VQE
#from qiskit.aqua.components.optimizers import L_BFGS_B
#optimizer = L_BFGS_B()
# optimizer = SPSA(maxiter=200)
optimizer = COBYLA(maxiter=1, tol=1e3)
# setup the initial state for the variational form
from qiskit.chemistry.components.initial_states import HartreeFock
init_state = HartreeFock(num_spin_orbitals, num_particles)
# setup the variational form for VQE
from qiskit.circuit.library import TwoLocal
var_form = TwoLocal(num_qubits, ['ry', 'rz'], 'cz', initial_state=init_state)
# setup and run VQE
from qiskit.aqua.algorithms import VQE
algorithm = VQE(qubit_op, var_form, optimizer, quantum_instance=qi)
# set the backend for the quantum computation
start_time = time.time()
result = algorithm.run()#backend)
end_time = time.time()
print("Execution Time: %s" % (end_time - start_time))
