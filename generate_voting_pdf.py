import os
import pypdf
from xhtml2pdf import pisa

def build_pdf():
    assets_dir = os.path.abspath("assets")
    logo_path = os.path.join(assets_dir, "college_logo_0.png").replace("\\", "/")
    fig1_path = os.path.join(assets_dir, "fig_voting_arch.png").replace("\\", "/")
    fig2_path = os.path.join(assets_dir, "fig_voting_lifecycle.png").replace("\\", "/")
    fig3_path = os.path.join(assets_dir, "fig_gas_analysis.png").replace("\\", "/")

    html_content = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
@page cover_template {
    size: letter portrait;
    margin: 15mm;
    @frame content_frame {
        left: 18mm; width: 180mm; top: 12mm; height: 255mm;
    }
}

@page body_template {
    size: letter portrait;
    margin: 16mm;
    @frame header_frame {
        -pdf-frame-content: page_header;
        left: 18mm; width: 180mm; top: 8mm; height: 11mm;
    }
    @frame content_frame {
        left: 18mm; width: 180mm; top: 20mm; height: 240mm;
    }
    @frame footer_frame {
        -pdf-frame-content: page_footer;
        left: 18mm; width: 180mm; top: 263mm; height: 10mm;
    }
}

body {
    font-family: "Times New Roman", Times, serif;
    font-size: 9pt;
    line-height: 1.32;
    color: #111111;
}

.header-table {
    width: 100%;
    font-size: 8.5pt;
    color: #333333;
    border-bottom: 0.75pt solid #555555;
    padding-bottom: 2px;
}

.footer-table {
    width: 100%;
    font-size: 8pt;
    color: #444444;
    border-top: 0.75pt solid #888888;
    padding-top: 2px;
}

h1, h2, h3, h4 {
    font-family: "Times New Roman", Times, serif;
    color: #111111;
    margin: 0;
    padding: 0;
}

h2.section-title {
    font-size: 11pt;
    font-weight: bold;
    text-transform: uppercase;
    margin-top: 6px;
    margin-bottom: 3px;
    border-bottom: 0.5pt solid #444444;
    padding-bottom: 1.5px;
}

h3.sub-title {
    font-size: 9.5pt;
    font-weight: bold;
    margin-top: 5px;
    margin-bottom: 2px;
}

p {
    margin: 0 0 4px 0;
    text-align: justify;
}

ul, ol {
    margin: 2px 0 4px 14px;
    padding: 0;
}

li {
    margin-bottom: 1.5px;
    text-align: justify;
}

table.data-table {
    width: 100%;
    border-collapse: collapse;
    margin: 3px 0 5px 0;
    font-size: 8pt;
}

table.data-table th {
    background-color: #2b3a4a;
    color: #ffffff;
    font-weight: bold;
    padding: 3px 4px;
    border: 0.5pt solid #444444;
    text-align: left;
}

table.data-table td {
    padding: 2.5px 4px;
    border: 0.5pt solid #bbbbbb;
    vertical-align: middle;
}

table.data-table tr.even {
    background-color: #f7f9fa;
}

.text-center {
    text-align: center;
}

.bold {
    font-weight: bold;
}

.caption {
    font-size: 7.5pt;
    color: #444444;
    font-style: italic;
    text-align: center;
    margin-top: 2px;
    margin-bottom: 4px;
}

.img-container {
    text-align: center;
    margin: 3px 0 1px 0;
}

.code-box {
    background-color: #f8f9fa;
    border-left: 2.5pt solid #2b3a4a;
    padding: 3px 6px;
    margin: 3px 0;
    font-family: "Courier New", Courier, monospace;
    font-size: 7.8pt;
    line-height: 1.25;
}

.cover-wrapper {
    text-align: center;
    height: 100%;
}

.cover-univ {
    font-size: 15.5pt;
    font-weight: bold;
    margin-top: 8px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.cover-college {
    font-size: 13pt;
    font-weight: bold;
    margin-top: 6px;
}

.cover-addr {
    font-size: 10pt;
    margin-top: 3px;
}

.cover-naac {
    font-size: 10.5pt;
    font-weight: bold;
    margin-top: 3px;
    letter-spacing: 0.5px;
}

.cover-dept {
    font-size: 12pt;
    font-weight: bold;
    margin-top: 5px;
    letter-spacing: 0.5px;
}

.cover-logo {
    margin-top: 18px;
    margin-bottom: 16px;
}

.cover-rep-title {
    font-size: 13.5pt;
    font-weight: bold;
    letter-spacing: 1px;
    margin-top: 6px;
}

.cover-on {
    font-size: 11pt;
    font-weight: bold;
    margin-top: 5px;
}

.cover-project-title {
    font-size: 14.5pt;
    font-weight: bold;
    font-style: italic;
    color: #1a2a3a;
    margin-top: 8px;
    line-height: 1.3;
}

.cover-acad {
    font-size: 10.5pt;
    font-weight: bold;
    margin-top: 16px;
}

.cover-deg {
    font-size: 11pt;
    font-weight: bold;
    margin-top: 4px;
}

.cover-sub-by {
    font-size: 11pt;
    font-weight: bold;
    font-style: italic;
    margin-top: 22px;
}

.cover-single-member {
    margin-top: 8px;
    font-size: 11pt;
    font-weight: bold;
}

.cover-guide {
    margin-top: 26px;
    font-size: 10pt;
    line-height: 1.35;
}
</style>
</head>
<body>

<div id="page_header">
    <table class="header-table">
        <tr>
            <td align="left" style="width: 78%; font-weight: bold;">BlockVote: Decentralized E-Voting System Using Ethereum &amp; Web3</td>
            <td align="right" style="width: 22%;">Page <pdf:pagenumber></td>
        </tr>
    </table>
</div>

<div id="page_footer">
    <table class="footer-table">
        <tr>
            <td align="left" style="width: 75%;">Department of Computer Engineering, MESWCOE Pune</td>
            <td align="right" style="width: 25%;">Academic Year 2026-27</td>
        </tr>
    </table>
</div>

<!-- ================= PAGE 1: COVER PAGE ================= -->
<pdf:nexttemplate name="cover_template" />
<div class="cover-wrapper">
    <div class="cover-univ">Savitribai Phule Pune University</div>
    <div class="cover-college">Modern Education Society’s Wadia College of Engineering, Pune</div>
    <div class="cover-addr">19, Bund Garden, V.K. Joag Path, Pune – 411001.</div>
    <div class="cover-naac">ACCREDITED BY NBA AND NAAC WITH ‘A++’ GRADE</div>
    <div class="cover-dept">DEPARTMENT OF COMPUTER ENGINEERING</div>
    
    <div style="border-bottom: 1.5pt solid #111111; margin: 12px 30px 14px 30px;"></div>

    <div class="cover-logo">
        <img src="REPLACE_LOGO_PATH" height="110" alt="College Logo" />
    </div>

    <div class="cover-rep-title">A MINI-PROJECT REPORT</div>
    <div class="cover-on">ON</div>
    <div class="cover-project-title">“BlockVote: Decentralized E-Voting System Using Ethereum Smart Contracts &amp; Web3”</div>

    <div class="cover-acad">(Academic Year: 2026-27)</div>
    <div class="cover-deg">B.E. (COMPUTER ENGINEERING)</div>

    <div class="cover-sub-by">SUBMITTED BY:</div>
    <div class="cover-single-member">
        Aadish Sonawane &nbsp;&nbsp; (Roll No: F23112052)
    </div>

    <div class="cover-guide">
        <div class="bold" style="font-size: 10.5pt;">Under the Guidance of:</div>
        <div>Faculty of Computer Engineering</div>
        <div>Department of Computer Engineering</div>
        <div>Modern Education Society’s Wadia College of Engineering, Pune</div>
    </div>
</div>

<!-- ================= PAGE 2: INDEX + INTRO + PROBLEM + OBJECTIVES ================= -->
<pdf:nexttemplate name="body_template" />
<pdf:nextpage />
<div>
    <h2 style="font-size: 12pt; text-align: center; font-weight: bold; margin-bottom: 6px; letter-spacing: 0.5px;">INDEX</h2>
    
    <table class="data-table" style="font-size: 8pt; margin-bottom: 8px;">
        <thead>
            <tr>
                <th style="width: 12%; text-align: center;">Sr. No.</th>
                <th style="width: 74%;">CONTENTS</th>
                <th style="width: 14%; text-align: center;">Page No.</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td class="text-center bold">1</td>
                <td class="bold">Introduction &amp; Background</td>
                <td class="text-center bold">2</td>
            </tr>
            <tr class="even">
                <td class="text-center bold">2</td>
                <td class="bold">Problem Statement &amp; Project Objectives</td>
                <td class="text-center bold">2</td>
            </tr>
            <tr>
                <td class="text-center bold">3</td>
                <td class="bold">System Architecture &amp; Execution Pipeline</td>
                <td class="text-center bold">3</td>
            </tr>
            <tr class="even">
                <td class="text-center bold">4</td>
                <td class="bold">Technologies Used &amp; Software Stack</td>
                <td class="text-center bold">3</td>
            </tr>
            <tr>
                <td class="text-center bold">5</td>
                <td class="bold">Smart Contract Design &amp; Implementation (Voting.sol)</td>
                <td class="text-center bold">4</td>
            </tr>
            <tr class="even">
                <td class="text-center bold">6</td>
                <td class="bold">Web3 Frontend Client &amp; MetaMask Integration (index.html)</td>
                <td class="text-center bold">5</td>
            </tr>
            <tr>
                <td class="text-center bold">7</td>
                <td class="bold">Security Analysis, Verification &amp; Gas Cost Evaluation</td>
                <td class="text-center bold">6</td>
            </tr>
            <tr class="even">
                <td class="text-center bold">8</td>
                <td class="bold">Conclusion, Future Enhancements &amp; References</td>
                <td class="text-center bold">6</td>
            </tr>
        </tbody>
    </table>

    <h2 class="section-title">1. INTRODUCTION &amp; BACKGROUND</h2>
    <p>
        Electoral integrity represents the cornerstone of democratic governance and institutional trust. Traditional voting mechanisms—ranging from paper ballots to centralized electronic voting machines (EVMs) and web portals—suffer from systemic vulnerabilities: physical ballot stuffing, insider tampering, lack of independent voter auditability, and single points of failure.
    </p>
    <p>
        <b>Blockchain technology</b> provides a decentralized, append-only, cryptographically secured ledger that redefines electronic voting. By deploying election rules into an immutable Ethereum smart contract, voting logic executes autonomously without intermediaries. Every vote constitutes an on-chain transaction signed by a registered cryptographic wallet (MetaMask), providing absolute non-repudiation, verifiable tallying, and tamper-proof finality.
    </p>

    <h2 class="section-title">2. PROBLEM STATEMENT &amp; PROJECT OBJECTIVES</h2>
    <h3 class="sub-title">2.1 Problem Statement</h3>
    <div style="background-color: #f4f6f8; border-left: 2.5pt solid #2b3a4a; padding: 4px 7px; margin: 3px 0 5px 0; font-style: italic; font-size: 8.5pt;">
        “To design, implement, and evaluate a decentralized electronic voting application (dApp) utilizing an Ethereum Solidity smart contract and a Web3 client interface that enforces single-vote integrity, restricts administrative actions via role-based access control, and delivers real-time, tamper-proof ballot tallying.”
    </div>

    <h3 class="sub-title">2.2 Project Objectives</h3>
    <ul>
        <li><b>Develop an Immutable Smart Contract:</b> Author a gas-optimized contract in Solidity (^0.8.20) managing candidates, voter registration, and lifecycle state flags.</li>
        <li><b>Enforce Strict Access Control:</b> Implement an <code>onlyAdmin</code> modifier restricting candidate nomination, voter whitelisting, and voting session toggling to the deployer.</li>
        <li><b>Prevent Double-Voting &amp; Sybil Manipulation:</b> Track voter state in a persistent <code>mapping(address =&gt; Voter)</code>, ensuring strictly one vote per whitelisted cryptographic address.</li>
        <li><b>Build a Responsive Web3 Client:</b> Create an accessible frontend using HTML5, modern CSS, and <code>ethers.js</code> (v5.7.2) connecting seamlessly with MetaMask.</li>
        <li><b>Provide Real-Time Transparent Tallies:</b> Dynamically compute candidate vote percentages, update progress bars, and announce the winning candidate on-chain.</li>
    </ul>
</div>

<!-- ================= PAGE 3: ARCHITECTURE & TECH STACK ================= -->
<pdf:nexttemplate name="body_template" />
<pdf:nextpage />
<div>
    <h2 class="section-title">3. SYSTEM ARCHITECTURE &amp; EXECUTION PIPELINE</h2>
    <p>
        The BlockVote system is structured into a decoupled two-tier Web3 architecture comprising the <b>On-Chain Decentralized Layer</b> (Ethereum EVM) and the <b>Client Presentation Layer</b> (MetaMask + Browser DOM):
    </p>

    <div class="img-container">
        <img src="REPLACE_FIG1_PATH" width="480" height="180" alt="System Architecture" />
    </div>
    <div class="caption">Figure 1: Two-Tier System Architecture of BlockVote (Client Web3 Interface &amp; Ethereum EVM Contract).</div>

    <h3 class="sub-title">3.1 End-to-End Execution Stages</h3>
    <ol>
        <li><b>Contract Deployment:</b> The election officer deploys <code>Voting.sol</code> to the Ethereum network (local Hardhat/Ganache or testnet). The constructor records <code>admin = msg.sender</code>.</li>
        <li><b>Administrative Setup:</b> The admin nominates candidates via <code>addCandidate()</code> and whitelists authorized voter public keys via <code>registerVoter()</code> while voting is closed.</li>
        <li><b>Election Activation:</b> Once at least two candidates are registered, the admin calls <code>startVoting()</code>, flipping <code>votingOpen = true</code> and broadcasting a <code>VotingStarted()</code> event.</li>
        <li><b>Voter Connection &amp; Role Resolution:</b> Voters open <code>index.html</code>, connect their MetaMask wallet, and input the contract address. The dApp queries the contract via RPC to determine the active role (Admin or Voter) and conditionally renders the admin panel.</li>
        <li><b>Vote Casting &amp; Mining:</b> Eligible voters select a candidate and sign an Ethereum transaction via MetaMask calling <code>vote(_candidateId)</code>. The EVM validates eligibility, marks the voter as voted, increments the tally, and emits the <code>Voted</code> event upon block inclusion.</li>
        <li><b>Real-Time Result Auditing:</b> The client listens for block events and invokes <code>getCandidates()</code> and <code>winner()</code> to update vote tallies and animated percentage bars.</li>
    </ol>

    <h2 class="section-title">4. TECHNOLOGIES USED &amp; SOFTWARE STACK</h2>
    <table class="data-table">
        <thead>
            <tr>
                <th style="width: 25%;">Layer / Component</th>
                <th style="width: 25%;">Technology</th>
                <th style="width: 15%;">Version</th>
                <th style="width: 35%;">Functional Role</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td class="bold">Smart Contract Language</td>
                <td>Solidity</td>
                <td>^0.8.20</td>
                <td>State management, voting logic, and EVM bytecode execution.</td>
            </tr>
            <tr class="even">
                <td class="bold">Execution Environment</td>
                <td>Ethereum EVM</td>
                <td>London / Paris</td>
                <td>Decentralized consensus, transaction mining, and storage.</td>
            </tr>
            <tr>
                <td class="bold">Web3 Client Library</td>
                <td>ethers.js (UMD)</td>
                <td>5.7.2</td>
                <td>RPC communication, contract abstraction, and tx signing.</td>
            </tr>
            <tr class="even">
                <td class="bold">Crypto Wallet Provider</td>
                <td>MetaMask</td>
                <td>Latest</td>
                <td>Keypair management, account switching, and transaction signing.</td>
            </tr>
            <tr>
                <td class="bold">Frontend User Interface</td>
                <td>HTML5 / CSS3 / ES6</td>
                <td>Standard</td>
                <td>Responsive layout, dynamic candidate cards, and CSS bars.</td>
            </tr>
        </tbody>
    </table>
</div>

<!-- ================= PAGE 4: SMART CONTRACT DESIGN ================= -->
<pdf:nexttemplate name="body_template" />
<pdf:nextpage />
<div>
    <h2 class="section-title">5. SMART CONTRACT DESIGN &amp; IMPLEMENTATION (Voting.sol)</h2>
    <p>
        The smart contract <code>Voting.sol</code> encapsulates state variables, structs, mappings, modifiers, and functions implementing the complete election lifecycle.
    </p>

    <h3 class="sub-title">5.1 Core Data Structures &amp; Storage Layout</h3>
    <ul>
        <li><code>struct Candidate { uint256 id; string name; uint256 voteCount; }</code>: Stores unique candidate identifiers, names, and accumulated votes.</li>
        <li><code>struct Voter { bool registered; bool voted; uint256 votedFor; }</code>: Tracks registration status, double-voting prevention flags, and candidate choice.</li>
        <li><code>mapping(address =&gt; Voter) public voters;</code>: O(1) key-value hash table mapping Ethereum wallet addresses to their voter status.</li>
        <li><code>Candidate[] private candidates;</code>: Dynamic array holding all registered candidates.</li>
    </ul>

    <h3 class="sub-title">5.2 Election Lifecycle &amp; State Machine</h3>
    <div class="img-container">
        <img src="REPLACE_FIG2_PATH" width="460" height="115" alt="Election Lifecycle" />
    </div>
    <div class="caption">Figure 2: Three-Phase Finite State Machine of Voting.sol (Setup, Active, and Finalized).</div>

    <h3 class="sub-title">5.3 Access Control &amp; Method Specifications</h3>
    <table class="data-table">
        <thead>
            <tr>
                <th style="width: 24%;">Function Signature</th>
                <th style="width: 16%;">Visibility / Access</th>
                <th style="width: 60%;">Enforced Invariants &amp; Logic</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td class="bold">addCandidate(string)</td>
                <td>external onlyAdmin</td>
                <td>Requires <code>!votingOpen</code> and non-empty name string; appends candidate.</td>
            </tr>
            <tr class="even">
                <td class="bold">registerVoter(address)</td>
                <td>external onlyAdmin</td>
                <td>Verifies <code>!voters[_voter].registered</code>; sets registered flag to true.</td>
            </tr>
            <tr>
                <td class="bold">startVoting()</td>
                <td>external onlyAdmin</td>
                <td>Requires <code>candidates.length &gt;= 2</code> and <code>!votingOpen</code>; opens election.</td>
            </tr>
            <tr class="even">
                <td class="bold">endVoting()</td>
                <td>external onlyAdmin</td>
                <td>Requires <code>votingOpen == true</code>; closes election permanently.</td>
            </tr>
            <tr>
                <td class="bold">vote(uint256)</td>
                <td>external (public)</td>
                <td>Requires <code>votingOpen</code>, voter registered, not yet voted, and valid ID.</td>
            </tr>
            <tr class="even">
                <td class="bold">winner()</td>
                <td>external view</td>
                <td>Performs linear scan over candidates; returns index, name, and max votes.</td>
            </tr>
        </tbody>
    </table>

    <h3 class="sub-title">5.4 Security Mechanics</h3>
    <ul>
        <li><b>Checks-Effects-Interactions Pattern:</b> In <code>vote()</code>, <code>v.voted = true</code> is updated <i>before</i> incrementing vote counts, eliminating reentrancy vulnerabilities.</li>
        <li><b>Arithmetic Safety:</b> Compiled with Solidity <code>^0.8.20</code>, providing native revert on integer overflow and underflow without external SafeMath overhead.</li>
        <li><b>Administrative Segregation:</b> Candidate addition and voter whitelisting are blocked once voting begins, preventing ballot stuffing mid-election.</li>
    </ul>
</div>

<!-- ================= PAGE 5: DAPP FRONTEND INTEGRATION ================= -->
<pdf:nexttemplate name="body_template" />
<pdf:nextpage />
<div>
    <h2 class="section-title">6. WEB3 FRONTEND CLIENT &amp; METAMASK INTEGRATION (index.html)</h2>
    <p>
        The client interface is implemented as a single-page reactive decentralized application using vanilla HTML5, CSS3, and <code>ethers.js</code> (v5.7.2). It interacts directly with the browser's injected Ethereum provider (<code>window.ethereum</code>) without requiring centralized backend servers.
    </p>

    <h3 class="sub-title">6.1 Web3 Provider &amp; Signer Initialization</h3>
    <p>
        Upon clicking <b>Connect MetaMask</b>, the application requests user authorization via <code>eth_requestAccounts</code>. The Web3 provider wraps the provider instance, extracts the signer address, and initializes contract abstractions using the defined Application Binary Interface (ABI):
    </p>
    <div class="code-box">
        provider = new ethers.providers.Web3Provider(window.ethereum);<br>
        await provider.send("eth_requestAccounts", []);<br>
        signer = provider.getSigner();<br>
        contract = new ethers.Contract(contractAddress, ABI, signer);
    </div>

    <h3 class="sub-title">6.2 Role-Based Reactive Interface</h3>
    <p>
        The application queries <code>contract.admin()</code> and compares it to the connected wallet address:
    </p>
    <div class="code-box">
        isAdmin = admin.toLowerCase() === me.toLowerCase();<br>
        $("role").textContent = isAdmin ? "Admin" : "Voter";<br>
        $("adminCard").style.display = isAdmin ? "block" : "none";
    </div>
    <p>
        If the connected user is the deployer, the <b>Admin Panel</b> renders controls to add candidates, whitelist voter addresses, and toggle election states. For regular voter addresses, the admin panel remains strictly hidden.
    </p>

    <h3 class="sub-title">6.3 Live Ballot &amp; Dynamic CSS Bar Rendering</h3>
    <p>
        The client dynamically fetches the candidates array via <code>contract.getCandidates()</code>, calculates the total votes across all candidates, and derives individual vote shares:
    </p>
    <div class="code-box">
        const pct = total ? Math.round(n * 100 / total) : 0;<br>
        const canVote = open &amp;&amp; v.registered &amp;&amp; !v.voted;<br>
        // Button enabled only when: voting is open, voter is registered, and has not voted
    </div>
    <p>
        Candidate cards feature a stylized CSS bar (<code>height: 8px</code>) whose inner fill width transitions smoothly (<code>transition: width .4s</code>), providing instantaneous visual feedback of ballot trends.
    </p>

    <h3 class="sub-title">6.4 Asynchronous Transaction Pipeline &amp; Event Handling</h3>
    <p>
        All state-modifying operations (candidate creation, registration, voting) are managed through a unified <code>send(promise, okMsg)</code> helper that handles transaction submission, extracts transaction hashes, awaits block mining confirmations (<code>await tx.wait()</code>), and triggers a complete DOM refresh.
    </p>
    <p>
        Additionally, the dApp registers an account change listener (<code>window.ethereum.on("accountsChanged", () =&gt; location.reload())</code>), ensuring seamless interface resetting whenever the user switches active accounts in MetaMask.
    </p>
</div>

<!-- ================= PAGE 6: TESTING, GAS & CONCLUSION ================= -->
<pdf:nexttemplate name="body_template" />
<pdf:nextpage />
<div>
    <h2 class="section-title">7. SECURITY ANALYSIS, VERIFICATION &amp; GAS COST EVALUATION</h2>
    <h3 class="sub-title">7.1 Automated Verification &amp; Edge Case Testing</h3>
    <table class="data-table">
        <thead>
            <tr>
                <th style="width: 26%;">Test Scenario</th>
                <th style="width: 34%;">Input Condition / Invocation</th>
                <th style="width: 25%;">Expected EVM Response</th>
                <th style="width: 15%; text-align: center;">Result</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td class="bold">Legitimate Vote</td>
                <td>Registered voter calls <code>vote(0)</code> when open</td>
                <td>Vote recorded; event emitted</td>
                <td class="text-center bold" style="color: #1f9d63;">PASSED</td>
            </tr>
            <tr class="even">
                <td class="bold">Double Voting Attempt</td>
                <td>Voter attempts second call to <code>vote()</code></td>
                <td>Reverts: "You have already voted"</td>
                <td class="text-center bold" style="color: #1f9d63;">PASSED</td>
            </tr>
            <tr>
                <td class="bold">Unregistered Voter</td>
                <td>Non-whitelisted address calls <code>vote()</code></td>
                <td>Reverts: "Not a registered voter"</td>
                <td class="text-center bold" style="color: #1f9d63;">PASSED</td>
            </tr>
            <tr class="even">
                <td class="bold">Unauthorized Admin</td>
                <td>Non-admin calls <code>addCandidate()</code></td>
                <td>Reverts: "Only admin can do this"</td>
                <td class="text-center bold" style="color: #1f9d63;">PASSED</td>
            </tr>
            <tr>
                <td class="bold">Premature Start</td>
                <td>Admin calls <code>startVoting()</code> with 1 candidate</td>
                <td>Reverts: "Add at least 2 candidates"</td>
                <td class="text-center bold" style="color: #1f9d63;">PASSED</td>
            </tr>
        </tbody>
    </table>

    <h3 class="sub-title">7.2 Gas Consumption Benchmark</h3>
    <div class="img-container">
        <img src="REPLACE_FIG3_PATH" width="460" height="120" alt="Gas Analysis" />
    </div>
    <div class="caption">Figure 3: EVM Execution Gas Profile for Core Functions of Voting.sol.</div>

    <h2 class="section-title">8. CONCLUSION, FUTURE ENHANCEMENTS &amp; REFERENCES</h2>
    <h3 class="sub-title">8.1 Conclusion</h3>
    <p>
        The BlockVote project successfully demonstrates a fully functional, decentralized e-voting platform eliminating third-party reliance. By coupling a gas-conscious Solidity smart contract with a lightweight Web3 interface, the system guarantees single-vote integrity, robust role-based access control, and transparent public auditability.
    </p>

    <h3 class="sub-title">8.2 Future Enhancements</h3>
    <ul>
        <li><b>Zero-Knowledge Privacy (zk-SNARKs):</b> Integrate zk-proofs (e.g., Semaphore protocol) to conceal voter identities while verifying voter eligibility on-chain.</li>
        <li><b>Layer-2 Scalability:</b> Deploy to Arbitrum or Polygon zkEVM to reduce gas transaction costs by &gt;95%.</li>
        <li><b>Decentralized Identity (DID):</b> Connect Aadhaar/government credentials via Soulbound Tokens (SBTs) for automated biometric whitelisting.</li>
    </ul>

    <h3 class="sub-title">8.3 References</h3>
    <ol style="font-size: 7.5pt; margin-top: 1px;">
        <li><b>Wood, G. (2014).</b> <i>Ethereum: A secure decentralised generalised transaction ledger.</i> Ethereum Project Yellow Paper.</li>
        <li><b>Buterin, V. (2013).</b> <i>Ethereum: A Next-Generation Smart Contract and Decentralized Application Platform.</i> White Paper.</li>
        <li><b>OpenZeppelin (2024).</b> <i>Smart Contract Security Best Practices and Access Control Patterns.</i> <code>docs.openzeppelin.com</code></li>
        <li><b>Ethers.js (2024).</b> <i>Complete Ethereum Library and Wallet Implementation in JavaScript.</i> <code>docs.ethers.org</code></li>
        <li><b>SPPU (2026).</b> <i>Curriculum for Blockchain Technology &amp; Decentralized Applications, Department of Computer Engineering.</i></li>
    </ol>
</div>

</body>
</html>
"""

    html_content = html_content.replace("REPLACE_LOGO_PATH", logo_path)
    html_content = html_content.replace("REPLACE_FIG1_PATH", fig1_path)
    html_content = html_content.replace("REPLACE_FIG2_PATH", fig2_path)
    html_content = html_content.replace("REPLACE_FIG3_PATH", fig3_path)

    output_pdf_path = "BlockVote_Project_Report.pdf"
    with open(output_pdf_path, "wb") as f:
        pisa_status = pisa.CreatePDF(html_content, dest=f)

    if pisa_status.err:
        print(f"Error generating PDF: {pisa_status.err}")
        return False
    else:
        print(f"PDF generated successfully at {output_pdf_path} (size: {os.path.getsize(output_pdf_path)} bytes)")
        reader = pypdf.PdfReader(output_pdf_path)
        print(f"Total page count: {len(reader.pages)}")
        for i, page in enumerate(reader.pages):
            txt = page.extract_text()
            first_line = txt.split('\n')[0].strip() if txt else 'EMPTY'
            print(f"Page {i+1} ({len(txt)} chars): {first_line[:80]}")
        return True

if __name__ == "__main__":
    build_pdf()
