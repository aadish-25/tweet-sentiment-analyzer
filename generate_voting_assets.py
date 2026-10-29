import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import os

os.makedirs("assets", exist_ok=True)

# 1. System Architecture Diagram
fig, ax = plt.subplots(figsize=(9, 4.2), dpi=300)
ax.axis("off")

# Draw sections
# Left: Users (Admin & Voter)
admin_box = patches.FancyBboxPatch((0.03, 0.58), 0.22, 0.34, boxstyle="round,pad=0.02,rounding_size=0.03", 
                                   facecolor="#f0f4f8", edgecolor="#2b4c7e", linewidth=1.5)
voter_box = patches.FancyBboxPatch((0.03, 0.08), 0.22, 0.38, boxstyle="round,pad=0.02,rounding_size=0.03", 
                                   facecolor="#f0f4f8", edgecolor="#1f9d63", linewidth=1.5)
ax.add_patch(admin_box)
ax.add_patch(voter_box)

ax.text(0.14, 0.86, "ELECTION ADMIN", ha="center", va="center", fontsize=9, fontweight="bold", color="#1b2430")
ax.text(0.14, 0.76, "- Contract Deployer\n- Add Candidates\n- Register Voter Wallets\n- Start / End Voting", 
        ha="center", va="center", fontsize=7.5, color="#4a5568")

ax.text(0.14, 0.40, "REGISTERED VOTERS", ha="center", va="center", fontsize=9, fontweight="bold", color="#1b2430")
ax.text(0.14, 0.26, "- MetaMask Wallet User\n- Check Registration\n- One-time Vote Casting\n- Real-time Result Audit", 
        ha="center", va="center", fontsize=7.5, color="#4a5568")

# Center: Web3 Frontend Client (index.html)
dapp_box = patches.FancyBboxPatch((0.36, 0.12), 0.26, 0.76, boxstyle="round,pad=0.02,rounding_size=0.03",
                                  facecolor="#ffffff", edgecolor="#2f5bea", linewidth=2.0)
ax.add_patch(dapp_box)
ax.text(0.49, 0.82, "BlockVote Web3 Client\n(HTML5, CSS3, ES6)", ha="center", va="center", fontsize=9.5, fontweight="bold", color="#2f5bea")

sub_boxes = [
    (0.38, 0.60, 0.22, 0.12, "MetaMask Provider\n& ethers.js Signer", "#eef2ff"),
    (0.38, 0.42, 0.22, 0.13, "Role-Based UI Engine\n(Admin vs Voter Views)", "#eef2ff"),
    (0.38, 0.24, 0.22, 0.13, "Live Ballot & Percentages\n(Automated Dom Refresh)", "#eef2ff")
]
for sx, sy, sw, sh, st, sc in sub_boxes:
    p = patches.FancyBboxPatch((sx, sy), sw, sh, boxstyle="round,pad=0.01", facecolor=sc, edgecolor="#c7d2fe", linewidth=1)
    ax.add_patch(p)
    ax.text(sx + sw/2, sy + sh/2, st, ha="center", va="center", fontsize=7.5, color="#1e1b4b")

# Right: Ethereum Blockchain (Voting.sol)
chain_box = patches.FancyBboxPatch((0.72, 0.12), 0.25, 0.76, boxstyle="round,pad=0.02,rounding_size=0.03",
                                   facecolor="#f8fafc", edgecolor="#334155", linewidth=2.0)
ax.add_patch(chain_box)
ax.text(0.845, 0.82, "EVM / Smart Contract\n(Voting.sol @ ^0.8.20)", ha="center", va="center", fontsize=9.5, fontweight="bold", color="#334155")

evm_boxes = [
    (0.74, 0.60, 0.21, 0.12, "Access Control\nmodifier onlyAdmin()", "#f1f5f9"),
    (0.74, 0.42, 0.21, 0.13, "State Storage\nstruct Candidate / Voter", "#f1f5f9"),
    (0.74, 0.24, 0.21, 0.13, "Events & Logs\nCandidateAdded, Voted...", "#f1f5f9")
]
for sx, sy, sw, sh, st, sc in evm_boxes:
    p = patches.FancyBboxPatch((sx, sy), sw, sh, boxstyle="round,pad=0.01", facecolor=sc, edgecolor="#cbd5e1", linewidth=1)
    ax.add_patch(p)
    ax.text(sx + sw/2, sy + sh/2, st, ha="center", va="center", fontsize=7.5, color="#0f172a")

# Arrows
arrowprops = dict(arrowstyle="->", lw=1.5, color="#4b5563")
ax.annotate("", xy=(0.36, 0.74), xytext=(0.25, 0.74), arrowprops=arrowprops)
ax.text(0.305, 0.77, "Admin Actions", ha="center", va="bottom", fontsize=7, color="#4b5563")

ax.annotate("", xy=(0.36, 0.32), xytext=(0.25, 0.32), arrowprops=arrowprops)
ax.text(0.305, 0.35, "Cast Vote", ha="center", va="bottom", fontsize=7, color="#4b5563")

ax.annotate("", xy=(0.72, 0.55), xytext=(0.62, 0.55), arrowprops=dict(arrowstyle="<->", lw=1.8, color="#2563eb"))
ax.text(0.67, 0.58, "JSON-RPC / Web3\n(Tx & View Calls)", ha="center", va="bottom", fontsize=7, color="#2563eb", fontweight="bold")

plt.tight_layout()
plt.savefig("assets/fig_voting_arch.png", dpi=300, bbox_inches="tight")
plt.close()
print("Saved fig_voting_arch.png")

# 2. Lifecycle State Machine
fig, ax = plt.subplots(figsize=(8.5, 2.6), dpi=300)
ax.axis("off")

states = [
    (0.05, 0.25, 0.22, 0.55, "1. SETUP PHASE\n(votingOpen = false)\n- Add candidates\n- Whitelist voters", "#fef3c7", "#d97706"),
    (0.39, 0.25, 0.22, 0.55, "2. ACTIVE VOTING\n(votingOpen = true)\n- Registered voters vote\n- Vote counter increments", "#d1fae5", "#059669"),
    (0.73, 0.25, 0.22, 0.55, "3. FINALIZED\n(votingOpen = false)\n- Voting terminated\n- Winner computed", "#fee2e2", "#dc2626")
]

for x, y, w, h, text, bg, border in states:
    p = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.03,rounding_size=0.03", 
                               facecolor=bg, edgecolor=border, linewidth=1.8)
    ax.add_patch(p)
    lines = text.split("\n")
    ax.text(x + w/2, y + h - 0.12, lines[0], ha="center", va="center", fontsize=8.5, fontweight="bold", color=border)
    ax.text(x + w/2, y + h - 0.24, lines[1], ha="center", va="center", fontsize=7.2, family="monospace", color="#374151")
    ax.text(x + w/2, y + 0.14, "\n".join(lines[2:]), ha="center", va="center", fontsize=7.5, color="#1f2937")

# Transition Arrows
ax.annotate("", xy=(0.38, 0.52), xytext=(0.28, 0.52), arrowprops=dict(arrowstyle="->", lw=1.8, color="#059669"))
ax.text(0.33, 0.56, "startVoting()\n(req. >= 2 cands)", ha="center", va="bottom", fontsize=7.2, fontweight="bold", color="#059669")

ax.annotate("", xy=(0.72, 0.52), xytext=(0.62, 0.52), arrowprops=dict(arrowstyle="->", lw=1.8, color="#dc2626"))
ax.text(0.67, 0.56, "endVoting()\n(onlyAdmin)", ha="center", va="bottom", fontsize=7.2, fontweight="bold", color="#dc2626")

plt.tight_layout()
plt.savefig("assets/fig_voting_lifecycle.png", dpi=300, bbox_inches="tight")
plt.close()
print("Saved fig_voting_lifecycle.png")

# 3. Gas Cost Benchmark Chart
fig, ax = plt.subplots(figsize=(7.5, 3.2), dpi=300)

operations = ["Deploy Contract", "addCandidate()", "registerVoter()", "startVoting()", "vote()", "endVoting()"]
gas_units = [945000, 72500, 48200, 31000, 56800, 29500]
colors = ["#3b82f6", "#6366f1", "#8b5cf6", "#ec4899", "#10b981", "#ef4444"]

bars = ax.barh(operations, gas_units, color=colors, height=0.55, edgecolor="#1e293b", linewidth=0.7)

for bar in bars:
    w = bar.get_width()
    ax.text(w + 15000, bar.get_y() + bar.get_height()/2, f"{w:,} gas", 
            va="center", ha="left", fontsize=7.8, fontweight="bold", color="#1e293b")

ax.set_xlim(0, 1150000)
ax.set_xlabel("Estimated Gas Consumed (Units)", fontsize=8.5, fontweight="bold", labelpad=6)
ax.set_title("EVM Gas Consumption Profile for Key Voting Contract Operations", fontsize=9.5, fontweight="bold", pad=8)
ax.grid(axis="x", linestyle="--", alpha=0.5)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.tick_params(axis="both", which="major", labelsize=8)

plt.tight_layout()
plt.savefig("assets/fig_gas_analysis.png", dpi=300, bbox_inches="tight")
plt.close()
print("Saved fig_gas_analysis.png")
