---
# ═══════════════════════════════════════════════════════════════════
# GROUP 1: CORE IDENTITY
# ═══════════════════════════════════════════════════════════════════
id: pat_01kjj4j5hcfy8at1kxb5xsga3e
slug: distributed-problem-solving
title: "Distributed Problem Solving"
aliases: ["Crowdsourcing", "Collective Intelligence", "Open Innovation"]
summary: >-
  This pattern outsources a task or problem to a large, undefined community, typically via the internet. It leverages the collective intelligence of the crowd to generate diverse solutions, with contributors often receiving small rewards or prizes.
# ═══════════════════════════════════════════════════════════════════
# GROUP 2: CONTEXTUAL TRANSLATION (The Navigator Engine)
# ═══════════════════════════════════════════════════════════════════
context_labels:
  corporate: "Leveraging open innovation platforms to solve R&D challenges and source new product ideas from a global talent pool."
  government: "Using citizen science and public consultations to gather data, inform policy, and solve civic problems more inclusively."
  activist: "Mobilizing volunteers for distributed campaigns, such as mapping environmental data or monitoring human rights violations."
  tech: "Building platforms that facilitate the matching of complex problems with a distributed network of solvers, often using bounties or contests."
  academic: "Conducting large-scale research projects by distributing data collection and analysis tasks among a network of participants."
# ═══════════════════════════════════════════════════════════════════
# GROUP 3: ONTOLOGY & SEARCH OPTIMIZATION (The RAG Fuel)
# ═══════════════════════════════════════════════════════════════════
ontology:
  domain: business
  cross_domains: ["technology", "social-organization"]
  search_hints:
    primary_tension: "Centralized, internal expertise vs. decentralized, external knowledge networks."
    vector_keywords: ["crowdsourcing", "open innovation", "collective intelligence", "distributed work", "gig economy", "problem solving", "innovation contest", "citizen science"]
  commons_assessment:
    stakeholder_architecture: 4
    value_creation: 4
    resilience: 3
    ownership: 1
    autonomy: 2
    composability: 4
    fractal_value: 3
    vitality: 3.0
    vitality_reasoning: >-
      The pattern shows high vitality in its ability to create value through a broad stakeholder base. However, its vitality is constrained by a low ownership score, as value is often captured centrally by the platform owner rather than being distributed back to the contributors who co-created it. This extractive model can undermine long-term community engagement and resilience.
    overall_score: 3.0
# ═══════════════════════════════════════════════════════════════════
# GROUP 4: LIFECYCLE & CONFIDENCE
# ═══════════════════════════════════════════════════════════════════
lifecycle:
  usage_stage: application
  adoption_stage: mainstream
  status: draft
  version: "0.1"
  confidence: 2
# ═══════════════════════════════════════════════════════════════════
# GROUP 5: HARD RELATIONSHIPS (Human-Curated Graph)
# ═══════════════════════════════════════════════════════════════════
relationships:
  generalizes_from: []
  specializes_to: []
  enables:
    - slug: open-source
      weight: 0.7
  requires:
    - slug: digital-platform
      weight: 0.9
  alternatives:
    - slug: expert-consulting
      weight: 0.8
  complementary:
    - slug: community-engagement
      weight: 0.6
  tools: []
# ═══════════════════════════════════════════════════════════════════
# GROUP 6: GRAPH GARDEN (Machine-Written Graph)
# ═══════════════════════════════════════════════════════════════════
graph_garden:
  last_pruned: 2026-02-28
  entities:
    - id: Q750429
      type: concept
      label: "Open innovation"
      relevance: 0.9
    - id: Q152066
      type: concept
      label: "Collective intelligence"
      relevance: 0.9
    - id: Q273760
      type: practice
      label: "Citizen science"
      relevance: 0.8
    - id: Q422150
      type: concept
      label: "Gig worker"
      relevance: 0.7
  communities:
    - id: business-model-innovation
      label: "Business Model Innovation"
      source: taxonomy
      confidence: 0.9
# ═══════════════════════════════════════════════════════════════════
# GROUP 7: PROVENANCE
# ═══════════════════════════════════════════════════════════════════
contributors: ["higgerix", "cloudsters"]
sources:
  - "Oliver Gassmann, Karolin Frankenberger & Michaela Csik, The Business Model Navigator (2014)"
  - "businessmodelnavigator.com — Pattern #9: Crowdsourcing"
license: CC-BY-SA-4.0
attribution: "commons.engineering by cloudsters, https://cloudsters.net"
collection: bmn-gassmann
---
> The power of many minds outweighs the power of a few.
> [!NOTE] Confidence Rating: ★★ (Medium)
> This pattern is well-documented in business literature and widely observed in practice through platforms like Kaggle and Innocentive. However, its long-term sustainability and ethical implications are still subjects of ongoing debate.
---
### Section 1: Context
The traditional model of innovation has been an internal, closed-door process. Organizations relied on their in-house R&D departments, believing that the most valuable expertise resided within their own walls. This approach, however, is increasingly challenged in a world of accelerating technological change and globalized knowledge. The cost of maintaining large, specialized R&D teams can be prohibitive, and even the most brilliant internal teams can suffer from a lack of diverse perspectives, leading to groupthink and incremental, rather than breakthrough, innovation.

The rise of the internet and digital platforms has fundamentally altered this landscape. It created a hyper-connected global network where knowledge and talent are distributed. This connectivity makes it possible to tap into a vast, external pool of expertise at a scale previously unimaginable. The Distributed Problem Solving pattern emerges from this context, providing a mechanism to move beyond the limitations of the firm and leverage a global brain to tackle complex challenges.
---
### Section 2: Problem
Organizations frequently face problems that are either outside their core competencies or require a novel approach that internal teams are ill-equipped to provide. Relying solely on internal resources can be slow, expensive, and risky. Hiring specialized consultants is an alternative, but it is also costly and scales poorly. The core problem, therefore, is how to access a wide range of diverse, specialized knowledge quickly and cost-effectively to generate superior solutions.

Furthermore, many problems benefit from a sheer volume of attempts and a diversity of approaches. A single internal team, no matter how skilled, is limited in the number of hypotheses it can explore. This is particularly true for "wicked problems" that are ill-defined and have no single optimal solution. The challenge is to create a system that can orchestrate a massive, parallel search of the solution space without incurring massive coordination overhead.
---
### Section 3: Solution
The Distributed Problem Solving pattern addresses this by externalizing the innovation process. Instead of assigning a problem to an internal team, an organization broadcasts an open call for solutions to a large and anonymous crowd. This is typically done through a digital platform that manages the process. The problem is carefully defined, along with the criteria for a successful solution and the incentives for contributing.

The core mechanism relies on incentive design. Contributors are motivated by a combination of factors, including monetary rewards, the chance to win a significant prize, public recognition, or the intrinsic satisfaction of solving a challenging problem. By turning the problem into a competition or a paid task, the organization can attract a large number of participants with diverse backgrounds, skills, and perspectives. This diversity is the key to unlocking novel solutions that would not have emerged from a more homogeneous group. The platform then provides a framework for submitting, evaluating, and selecting the most promising solutions, effectively filtering the signal from the noise.
---
### Section 4: Implementation
Successfully implementing this pattern requires several key steps. First, the problem must be carefully articulated. It needs to be specific enough to be actionable but open enough to allow for creative solutions. The problem must be "modularized" so it can be worked on by individuals without deep knowledge of the organization's internal systems. Second, the right incentives must be chosen to attract the desired type of contributor. Small cash payments (micropayments) work for simple tasks, while larger prizes or bounties are necessary for complex R&D challenges.

Third, the right platform or channel must be selected to reach the target crowd. This could be a public platform like Kaggle for data science problems, a specialized innovation broker like Innocentive, or a custom-built portal. Finally, a clear and transparent process for evaluation and selection is critical to maintain the trust and engagement of the community. This includes defining intellectual property rights upfront, ensuring fair judging, and providing feedback to participants. Without a well-managed process, the organization risks damaging its reputation and losing access to the crowd's talent.
---
### Section 5: Consequences
The positive consequences of this pattern are significant. It can dramatically reduce the cost and time of R&D, provide access to a global talent pool, and generate a wide array of innovative solutions. It allows organizations to be more agile and responsive to market changes by tapping into external knowledge on demand. For contributors, it offers opportunities to earn income, develop skills, and work on interesting problems with a low barrier to entry.

However, there are also significant negative consequences and ethical considerations. From a commons perspective, this model is often extractive. The platform owner and the problem sponsor typically capture the vast majority of the value created, while the contributors receive a disproportionately small share. This can lead to the exploitation of "digital labor" and create a precarious workforce with few rights or protections. Furthermore, issues around intellectual property can be contentious, and the quality of solutions can be highly variable, requiring significant effort to filter and validate.
---
### Section 6: Known Uses
Several major corporations have successfully used this pattern to drive innovation. **Procter & Gamble's** "Connect + Develop" program is a classic example. Instead of relying solely on its 7,500 internal researchers, P&G opened its innovation pipeline to the outside world, sourcing ideas for products like the Olay Regenerist and the Swiffer Duster from external inventors and partners. This approach has allowed them to significantly increase their innovation success rate while reducing R&D costs.

**General Electric** has used crowdsourcing for its "Ecomagination Challenge," an open competition to find and fund the best ideas in green technology. By offering substantial prize money, GE attracted thousands of proposals from entrepreneurs, students, and researchers worldwide, leading to investments in promising new ventures. Similarly, **Cisco** has run innovation challenges like the "Cisco Innovation Grand Challenge" to source ideas from startups and individuals, helping the company stay ahead of technological trends and identify potential acquisition targets.
---
### Section 7: Cognitive Era
The Cognitive Era, driven by AI and massive data processing capabilities, is poised to supercharge the Distributed Problem Solving pattern. AI can play a crucial role in almost every stage of the process. For instance, AI can help in formulating and deconstructing complex problems into smaller, more manageable micro-tasks that are suitable for a distributed workforce. This allows for more complex challenges to be crowdsourced than ever before.

Furthermore, AI-powered platforms can become more sophisticated in matching problems with the right solvers based on their skills, past performance, and even cognitive styles. This improves the efficiency and quality of the outcomes. In the evaluation phase, AI can be used to perform initial screening of submissions, identify plagiarism, and even assess the novelty and feasibility of proposed solutions, reducing the burden on human evaluators. As generative AI becomes more powerful, it may even act as a collaborator or a tool for the crowd, helping them to prototype and iterate on their ideas more rapidly.
---
### Section 8: Vitality
**Signs of life:**
A healthy ecosystem for distributed problem solving shows a high level of engagement and a steady flow of new participants. The problems being posted are challenging and meaningful, attracting top talent. There is a sense of fair play, with clear rules, transparent evaluation, and rewards that are perceived as commensurate with the effort required. Successful platforms often foster a community aspect, where contributors can collaborate, learn from each other, and build their reputations. The pattern is thriving when organizations are not just using it for one-off contests but are integrating it as a continuous, strategic part of their innovation process.

**Signs of decay:**
The pattern begins to decay when it becomes purely transactional and extractive. If contributors feel that their work is being undervalued or that the system is rigged, they will disengage. Signs of decay include a decline in the quality and quantity of submissions, a high churn rate among participants, and a "race to the bottom" on pricing for tasks. Another sign of decay is when the platform becomes dominated by low-quality "solution mills" or automated bots, drowning out genuine contributions. If the overhead of managing and filtering the crowd's input starts to outweigh the benefits of their contributions, the model's vitality is severely compromised.
