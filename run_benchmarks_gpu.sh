#!/bin/bash


DATE=$(date +%Y%m%d)

DIR=$(pwd)
mkdir -p ${DIR}/${DATE}

#source ~/anaconda3/etc/profile.d/conda.sh
source /opt/conda/etc/profile.d/conda.sh
rqc_path=${DIR}/random_circ
#export AER_MULTI_GPU=1
nq_toy_circ=32
nq_random=32

conda activate QiskitDevenv
for app in qft graph_state hidden_linear_function quadratic_form iqp; do
    for q in ${nq_toy_circ}; do
        python run_benchmarks.py --num-qubits ${q} --app ${app} --fusion true > \
        ${DIR}/${DATE}/log.${app}.${q}.baseline_gpu_openmp.fusion.true
    done
done

for q in ${nq_toy_circ}; do
    python test_qaoa.py ${q} statevector_gpu > ${DIR}/${DATE}/log.qaoa.${q}.baseline_gpu_openmp.fusion.true
done

for q in ${nq_random}; do
    python run_benchmarks.py --num-qubits ${q} --app ${rqc_path}/circuit_n${q}_m14_s3_e0_pEFGH.qasm --fusion true > \
    ${DIR}/${DATE}/log.random_circuit.${q}.baseline_gpu_openmp.fusion.true
done

#nvprof -o chem.34.baseline_gpu_openmp.nvprof python hchain_vqe_single_iteration.py 18 gpu qasm > ${DIR}/${DATE}/log.chem.34.baseline_gpu_openmp.fusion.true
conda deactivate

conda activate Q-GPU-multi-gpu
for app in qft graph_state hidden_linear_function quadratic_form iqp; do
    for q in ${nq_toy_circ}; do
        python run_benchmarks.py --num-qubits ${q} --app ${app} --fusion true > \
        ${DIR}/${DATE}/log.${app}.${q}.multi_gpu.fusion.true
    done
done

for q in ${nq_toy_circ}; do
    python test_qaoa.py ${q} statevector_gpu > ${DIR}/${DATE}/log.qaoa.${q}.multi_gpu.fusion.true
done

for q in ${nq_random}; do
    python run_benchmarks.py --num-qubits ${q} --app ${rqc_path}/circuit_n${q}_m14_s3_e0_pEFGH.qasm --fusion true > \
    ${DIR}/${DATE}/log.random_circuit.${q}.multi_gpu.fusion.true
done

#nvprof -o chem.34.multi_gpu.nvprof python hchain_vqe_single_iteration.py 18 gpu qasm > ${DIR}/${DATE}/log.chem.34.multi_gpu.fusion.true
conda deactivate

# get final results
ls -l ${DIR}/${DATE}/log.* | awk '{print $NF}' | \
while read line; do
  app=$(echo "$line" | awk -F'.' '{print $2}')
  q=$(echo "$line" | awk -F'.' '{print $3}')
  env=$(echo "$line" | awk -F'.' '{print $4}')
  res=$(tail -1 $line | awk -F',' '{print $NF}')
  echo -e "${app}\t${q}\t${env}\t${res}"
done | sort -k3,3 | tee ${DIR}/${DATE}/final_res.txt