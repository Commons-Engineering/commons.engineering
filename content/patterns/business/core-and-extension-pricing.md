---
# ═══════════════════════════════════════════════════════════════════
# GROUP 1: CORE IDENTITY
# ═══════════════════════════════════════════════════════════════════
id: pat_01kjj4j5hcfy8at1kwtdrmat3f
slug: core-and-extension-pricing
title: "Core & Extension Pricing"
aliases: ["Add-on", "Modular Pricing", "Unbundling"]
summary: >-
  This pattern involves offering a basic core product at a low, competitive price while generating revenue from a wide range of optional add-ons, features, or services. Customers are initially attracted by the low entry cost but often end up paying significantly more to customize the offering to their specific needs, leading to a higher total price than anticipated.
# ═══════════════════════════════════════════════════════════════════
# GROUP 2: CONTEXTUAL TRANSLATION (The Navigator Engine)
# ═══════════════════════════════════════════════════════════════════
context_labels:
  corporate: "A modular product strategy where the base model is a loss-leader and profit margins are concentrated in optional upgrades and service packages."
  government: "A public service model where essential services are free or subsidized, but citizens pay fees for enhanced access, faster processing, or specialized support (e.g., premium passport services)."
  activist: "A campaign model offering a free, basic level of participation (e.g., signing a petition) with tiered, paid options for deeper engagement, merchandise, or access to exclusive content to fund operations."
  tech: "A platform-as-a-service (PaaS) or software-as-a-service (SaaS) model where a core API or application is cheap or free, but costs scale with usage, additional modules, support tiers, or data processing."
  academic: "A research model where access to foundational data or publications is open, but fees are charged for derivative datasets, analytical tools, or specialized workshops based on the core research."
# ═══════════════════════════════════════════════════════════════════
# GROUP 3: ONTOLOGY & SEARCH OPTIMIZATION (The RAG Fuel)
# ═══════════════════════════════════════════════════════════════════
ontology:
  domain: business
  cross_domains: []
  search_hints:
    primary_tension: "Initial Affordability vs. Total Cost of Ownership"
    vector_keywords: ["modular pricing", "add-on", "upselling", "feature gating", "core product", "extensions", "unbundling", "variable pricing", "customization"]
  commons_assessment:
    stakeholder_architecture: 2
    value_creation: 3
    resilience: 3
    ownership: 2
    autonomy: 2
    composability: 4
    fractal_value: 2
    vitality: 2.6
    vitality_reasoning: >-
      The pattern scores high on composability, as it is inherently modular. However, it often leads to vendor lock-in, reduced user autonomy, and opaque total costs, which runs counter to commons principles of transparency and shared ownership. Value is often captured asymmetrically by the provider.
    overall_score: 2.6
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
  specializes_to:
    - slug: razors-and-blades-pricing
      weight: 0.7
  enables:
    - slug: customer-lock-in
      weight: 0.9
  requires: []
  alternatives:
    - slug: all-inclusive-pricing
      weight: 0.8
    - slug: flat-rate-pricing
      weight: 0.7
  complementary:
    - slug: subscription-services
      weight: 0.8
  tools: []
# ═══════════════════════════════════════════════════════════════════
# GROUP 6: GRAPH GARDEN (Machine-Written Graph)
# ═══════════════════════════════════════════════════════════════════
graph_garden:
  last_pruned: 2026-02-28
  entities:
    - id: ent-modular-design
      type: concept
      label: "Modular Design"
      relevance: 0.9
    - id: ent-price-discrimination
      type: concept
      label: "Price Discrimination"
      relevance: 0.8
    - id: ent-vendor-lock-in
      type: practice
      label: "Vendor Lock-In"
      relevance: 0.85
    - id: ent-total-cost-of-ownership
      type: concept
      label: "Total Cost of Ownership (TCO)"
      relevance: 0.75
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
  - "businessmodelnavigator.com — Pattern #1: Add-on"
license: CC-BY-SA-4.0
attribution: "commons.engineering by cloudsters, https://cloudsters.net"
collection: bmn-gassmann
---
> The price of the ticket is only the beginning of the journey's cost.
> [!NOTE] Confidence Rating: ★★ (Medium)
> This pattern is widely documented in business literature and observable in numerous mainstream technology and service companies. The core mechanism is well-understood, though its long-term consequences on market dynamics are still being studied.
---
### Section 1: Context
The Core & Extension Pricing model thrives in markets where customer needs are diverse and not easily met by a single, monolithic product. It is particularly effective in complex technology sectors, software, and service industries where functionality can be logically segmented or "unbundled." The premise is to lower the barrier to entry for new customers by presenting an attractively priced core product. This initial offering is often functional but basic, serving as a platform or gateway into a broader ecosystem of capabilities.

This approach decouples the initial adoption decision from the full-featured usage decision. A company can gain a significant foothold in a market by making its core technology widely accessible. The competitive focus shifts from the feature-richness of the initial offering to the perceived value and flexibility of the ecosystem. The success of this model hinges on a strong, stable core product that provides genuine standalone value, creating a foundation upon which customers are willing to build by purchasing extensions.

---
### Section 2: Problem
The primary problem this pattern addresses is the "one-size-fits-all" dilemma. In heterogeneous markets, a single, feature-packed product can be overwhelming and overpriced for users with simple needs, while simultaneously being inadequate for power users who require specialized functionality. This creates a market gap where customers are forced to compromise, either by paying for features they don't use or by lacking the tools they truly need.

Furthermore, high upfront costs for comprehensive software or services can be a significant barrier to adoption, especially for small to medium-sized businesses or individual consumers. Potential customers may be hesitant to make a large investment in a product they have not fully evaluated for their specific use case. This slows down market penetration and creates friction in the sales cycle. The challenge is to align the price of a solution with the specific value a customer derives from it, on a case-by-case basis.

---
### Section 3: Solution
The solution is to modularize the offering into a core component and a series of optional extensions. The core product is priced aggressively—sometimes at or below cost—to maximize adoption and establish a user base. It provides essential functionality that solves a basic, common problem, making it independently useful. This core product acts as the "hook."

The profit engine of the model is the sale of extensions, which can be additional features, integrations, support tiers, higher usage limits, or professional services. Each extension is priced separately, allowing customers to construct a tailored solution that matches their exact requirements and budget. This creates a "pay-as-you-grow" model where the cost scales with the customer's needs and sophistication. The architecture of the product must be designed for extensibility, with clear APIs and integration points to ensure that adding modules is a seamless experience.

This model transforms the economic relationship from a single transaction to an ongoing journey. The vendor focuses on demonstrating the value of the next extension, while the customer benefits from a flexible, adaptable solution that evolves with them. However, it relies on the vendor's ability to create a compelling ecosystem of extensions that customers perceive as valuable enough to purchase.

---
### Section 4: Implementation
Successfully implementing this pattern requires a strategic approach to product design and marketing. First, a clear line must be drawn between the core product and the extensions. The core must be valuable enough on its own to attract and retain users, but limited enough to create a natural demand for the extensions. If the core is too generous, there will be no incentive to upgrade; if it is too crippled, it will be perceived as a "bait-and-switch" and damage the brand's reputation.

Second, the product architecture must be inherently modular. This means designing a stable, well-documented core with a robust API or plugin system. This not only facilitates the creation of first-party extensions but can also foster a third-party developer ecosystem, which further enhances the value of the platform (a complementary pattern). Pricing for each module must be carefully calibrated to reflect its value and the cost of development.

Finally, the marketing and sales strategy must shift from selling a product to cultivating a platform. The initial sale is just the beginning. The focus should be on customer success, education, and demonstrating the power of the ecosystem. This often involves content marketing, webinars, and case studies that showcase how different combinations of extensions can solve complex problems, subtly encouraging users to invest more over time.

---
### Section 5: Consequences
The positive consequences of this model include greater market penetration and customer choice. By lowering the initial cost, companies can attract a wider range of customers. Users benefit from the ability to pay only for the functionality they need, resulting in a more efficient allocation of their resources. This can foster innovation, as a modular platform allows for experimentation and the development of niche solutions by both the vendor and third-party developers.

However, the negative consequences can be significant from a commons perspective. The model can lead to a lack of price transparency, where the total cost of ownership is obscured and often much higher than initially perceived. This can create "bill shock" and customer resentment. More critically, it can lead to strong vendor lock-in. As a customer invests more in a specific ecosystem of extensions and builds workflows around them, the cost and complexity of switching to a competitor become prohibitively high. This reduces customer autonomy and can stifle competition.

This power imbalance allows the vendor to capture a disproportionate amount of the value created. The composability is often constrained within a walled garden, limiting the potential for true, open interoperability. While it appears to offer choice, the architecture often centralizes control and ownership with the platform provider.

---
### Section 6: Known Uses
This pattern is ubiquitous in the modern software industry. **Salesforce** is a canonical example, offering a core CRM platform with a vast AppExchange marketplace where customers can purchase thousands of specialized add-on applications to extend functionality. Similarly, **SAP** provides a core ERP system, and customers pay significant additional fees for industry-specific modules, advanced analytics, and other enterprise functions.

In the consumer space, the budget airline **Ryanair** has perfected this model. The initial ticket price is exceptionally low, but revenue is driven by charges for everything from checked baggage and seat selection to priority boarding and in-flight refreshments. The video game industry also uses this pattern, as seen with **Sega** and other console makers who sell the base hardware and then generate ongoing revenue from the sale of individual games and, more recently, downloadable content (DLC) and in-game microtransactions.

Cloud computing platforms like **Amazon Web Services (AWS)** are a massive-scale implementation of this model. AWS offers a set of core compute and storage services at competitive prices, but the bill grows as customers add on databases, machine learning services, content delivery networks, and countless other specialized tools. The flexibility is immense, but so is the potential for costs to spiral as usage and dependency on the ecosystem deepen.

---
### Section 7: Cognitive Era
The Cognitive Era, driven by AI and ubiquitous data, supercharges the Core & Extension Pricing model. AI can be used to create highly personalized and predictive upselling opportunities. By analyzing a user's behavior within the core product, an AI system can identify their unmet needs and proactively recommend the specific extension that would solve their next problem. This transforms the add-on from a passive item in a catalog to a just-in-time, intelligent suggestion, dramatically increasing conversion rates.

Furthermore, AI itself becomes a premium extension. A core software product might offer basic functionality, but AI-powered features—such as predictive analytics, natural language processing, or automated workflows—are gated behind a higher-priced tier or sold as separate modules. This creates a powerful new vector for monetization, as the value of AI-driven insights and automation is often very high. For example, a basic CRM is the core, but an AI-powered lead scoring engine is a lucrative add-on.

Digital transformation also enables more granular unbundling. Where a feature might have been a single, indivisible block of code, it can now be delivered as a microservice and priced on a per-call or per-use basis. This allows for extremely fine-grained versions of the Core & Extension model, where customers can assemble highly customized solutions from a palette of micro-services, further blurring the line between the core product and its extensions.

---
### Section 8: Vitality
**Signs of life:**
A healthy ecosystem built on this model shows a vibrant marketplace for third-party extensions, indicating that the core platform is open and valuable enough for others to build upon. Another positive sign is when customers actively share "recipes" or combinations of modules to solve common problems, demonstrating genuine engagement and value creation. The company will often highlight customer success and ROI from using the extensions, rather than focusing solely on the low price of the core offering. Pricing for add-ons is transparent, and there are clear upgrade paths.

**Signs of decay:**
The model is decaying when the core product becomes so stripped-down that it is virtually useless on its own, functioning purely as a "forced trial" or "bait-and-switch." Customer complaints about opaque billing, vendor lock-in, and the high total cost of ownership become widespread. The vendor may start bundling unpopular add-ons with essential ones to force adoption. A lack of third-party development and a high customer churn rate are also clear signs of decay, indicating that the ecosystem is not providing sustainable value and customers are actively seeking alternatives despite high switching costs.
