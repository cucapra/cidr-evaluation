import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
import seaborn as sns
from collections import defaultdict
import csv

sns.set_theme()

icarus = defaultdict(list)
verilator = defaultdict(list)
interp = {}
lowered = {}

with open("statistics/compilation-results.csv") as file:
    # compilation,stage,mean,median,stddev
    for entry in csv.DictReader(file):
        if entry["stage"] == "icarus-verilog":
            icarus[entry["compilation"]].append(
                (entry["mean"], entry["stddev"])
            )
        elif entry["stage"] == "verilog":
            verilator[entry["compilation"]].append(
                (entry["mean"], entry["stddev"])
            )

with open("statistics/simulation-results.csv") as file:
    for entry in csv.DictReader(file):
        if entry["stage"] == "interpreter":
            interp[entry["simulation"]] = (entry["mean"], entry["stddev"])
        elif entry["stage"] == "icarus-verilog":
            icarus[entry["simulation"]].append(
                (entry["mean"], entry["stddev"])
            )
        elif entry["stage"] == "verilog":
            verilator[entry["simulation"]].append(
                (entry["mean"], entry["stddev"])
            )

with open("statistics/simulation-fully-lowered-results.csv") as file:
    for entry in csv.DictReader(file):
        lowered[entry["simulation-fully-lowered"]] = (
            entry["mean"],
            entry["stddev"],
        )


def remove_linalg(name):
    if "Linear Algebra" in name:
        return name[len("Linear Algebra") + 1 :]
    else:
        return name


bench_order = [x for x in icarus.keys() if x not in ("LeNet")]


icarus_comp_mean = np.array(
    [float(icarus[bench][0][0]) for bench in bench_order]
)
icarus_comp_stddev = np.array(
    [float(icarus[bench][0][1]) for bench in bench_order]
)

verilator_comp_mean = np.array(
    [float(verilator[bench][0][0]) for bench in bench_order]
)
verilator_comp_stddev = np.array(
    [float(verilator[bench][0][1]) for bench in bench_order]
)

icarus_sim_mean = np.array(
    [float(icarus[bench][1][0]) for bench in bench_order]
)
icarus_sim_stddev = np.array(
    [float(icarus[bench][1][1]) for bench in bench_order]
)

verilator_sim_mean = np.array(
    [float(verilator[bench][1][0]) for bench in bench_order]
)
verilator_sim_stddev = np.array(
    [float(verilator[bench][1][1]) for bench in bench_order]
)

interp_sim_mean = np.array([float(interp[bench][0]) for bench in bench_order])
interp_sim_stddev = np.array(
    [float(interp[bench][1]) for bench in bench_order]
)

lowered_sim_mean = np.array(
    [float(lowered[bench][0]) for bench in bench_order]
)
lowered_sim_stddev = np.array(
    [float(lowered[bench][1]) for bench in bench_order]
)


width = 1.4
bench_order = [remove_linalg(x) for x in bench_order]

icarus_labels = [(x) * 4 for x in range(len(bench_order))]
verilator_labels = [i + width for i in icarus_labels]
interp_labels = [v + width for v in verilator_labels]
lowered_labels = [i + width for i in interp_labels]

colors = sns.color_palette("Set2")
edge_color = "dimgray"

axis_options = {"rotation": 90, "fontsize": "large"}
y_axis_options = {"fontsize": "large"}

legend_options = {"fontsize": "large"}
label_options = {"fontsize": "x-large"}
output_options = {"bbox_inches": "tight"}
subplot_options = {"figsize": (8, 5)}

fig2, ax2 = plt.subplots(**subplot_options)
ax2.bar(
    icarus_labels,
    icarus_comp_mean / interp_sim_mean,
    width,
    tick_label=bench_order,
    label="Icarus Compilation",
    log=True,
    color=colors[0],
    edgecolor=colors[0],
)
ax2.bar(
    verilator_labels,
    verilator_comp_mean / interp_sim_mean,
    width,
    tick_label=bench_order,
    label="Verilator Compilation",
    log=True,
    color=colors[1],
    edgecolor=colors[1],
)


ax2.bar(
    icarus_labels,
    icarus_sim_mean / interp_sim_mean,
    width,
    bottom=icarus_comp_mean / interp_sim_mean,
    tick_label=bench_order,
    label="Icarus Simulation",
    log=True,
    hatch="\\",
    fill=False,
    edgecolor=colors[0],
)

ax2.bar(
    verilator_labels,
    verilator_sim_mean / interp_sim_mean,
    width,
    bottom=verilator_comp_mean / interp_sim_mean,
    tick_label=bench_order,
    label="Verilator Simulation",
    log=True,
    hatch="\\",
    fill=False,
    edgecolor=colors[1],
)
plt.axhline(y=1, color="gray", linestyle="dashed")


ax2.set_ylabel("Normalized End-to-end time", **label_options)
ax2.set_xlabel("Benchmark program", **label_options)
ax2.legend(**legend_options)


plt.xticks(**axis_options)
plt.yticks(**y_axis_options)

plt.savefig("f1.pdf", **output_options)


fig3, ax3 = plt.subplots(**subplot_options)

ax3.bar(
    icarus_labels,
    icarus_sim_mean / interp_sim_mean,
    width,
    tick_label=bench_order,
    yerr=icarus_sim_stddev,
    label="Icarus Simulation",
    log=True,
    color=colors[0],
    edgecolor=colors[0],
)

ax3.bar(
    verilator_labels,
    verilator_sim_mean / interp_sim_mean,
    width,
    tick_label=bench_order,
    yerr=verilator_sim_stddev,
    label="Verilator Simulation",
    log=True,
    color=colors[1],
    edgecolor=colors[1],
)


plt.axhline(y=1, color="gray", linestyle="dashed")


ax3.set_ylabel("Normalized Simulation Time", **label_options)
ax3.set_xlabel("Benchmark program", **label_options)
ax3.legend(**legend_options)
plt.xticks(**axis_options)
plt.yticks(**y_axis_options)


plt.savefig("f2.pdf", **output_options)


fig4, ax4 = plt.subplots(**subplot_options)

ax4.bar(
    interp_labels,
    lowered_sim_mean / interp_sim_mean,
    width * 2,
    tick_label=bench_order,
    label="Interpreter (lowered) Simulation",
    log=True,
    color=colors[2],
    edgecolor=colors[2],
)

ax4.set_ylabel("Normalized Simulation Time", **label_options)
ax4.set_xlabel("Benchmark program", **label_options)
ax4.legend(**legend_options)


plt.axhline(y=1, color="gray", linestyle="dashed")
plt.xticks(**axis_options)
plt.yticks(**y_axis_options)


plt.savefig("f3.pdf", **output_options)


ntt_idx = bench_order.index("NTT 64")

print("icarus slowdown", stats.gmean(icarus_sim_mean / interp_sim_mean))
print("verilator slowdown", stats.gmean(verilator_sim_mean / interp_sim_mean))
print("interp slowdown", stats.gmean(interp_sim_mean / verilator_sim_mean))
print("lowered slowdown", stats.gmean(lowered_sim_mean / interp_sim_mean))


print(
    "icarus NTT slowdown", icarus_sim_mean[ntt_idx] / interp_sim_mean[ntt_idx]
)
print(
    "lowered NTT slowdown",
    lowered_sim_mean[ntt_idx] / interp_sim_mean[ntt_idx],
)
print(
    "interp NTT slowdown (relative to verilator)",
    interp_sim_mean[ntt_idx] / verilator_sim_mean[ntt_idx],
)


print(
    "verilator comp slowdown",
    stats.gmean(verilator_comp_mean / interp_sim_mean),
)

print("icarus max slowdown", max(icarus_sim_mean / interp_sim_mean))
print("lowered max slowdown", max(lowered_sim_mean / interp_sim_mean))


# print(stats.gmean(verilator_comp_mean / interp_sim_mean))
print("\n===LeNet Stats===")
print(
    f"Icarus Comp: {icarus['LeNet'][0][0]} \n stderr: {icarus['LeNet'][0][1]}\nIcarus Sim: {float(icarus['LeNet'][1][0])/60}\n stderr: {float(icarus['LeNet'][1][1])/60}",
)
print(
    f"Icarus Slowdown: {float(icarus['LeNet'][1][0]) / float(verilator['LeNet'][1][0])}\n"
)

print(
    f"Icarus Slowdown (interp): {float(icarus['LeNet'][1][0]) / float(interp['LeNet'][0])}\n"
)

print(
    f"verilator Comp: {verilator['LeNet'][0][0]} \n stderr: {verilator['LeNet'][0][1]}\nverilator Sim: {float(verilator['LeNet'][1][0])/60}\n stderr: {float(verilator['LeNet'][1][1])/60}\n",
)

print(
    f"interp Sim: {float(interp['LeNet'][0])/60}\n stderr: {float(interp['LeNet'][1])/60}",
)
print(
    f"interp Slowdown: {float(interp['LeNet'][0]) / float(verilator['LeNet'][1][0])}\n"
)
