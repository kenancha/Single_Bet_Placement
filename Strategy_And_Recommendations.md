### Why these 2 tests were selected for automation

**Flow 1 — UI: Place Bet**

This case was selected because it represents a core business functionality and can be executed repeatedly with predictable test data. Automating it provides fast regression coverage for the complete betting flow, including bet selection, stake entry, bet placement, and verification that the betting receipt is generated correctly.

It is also a good candidate for automation because it can detect regressions in the UI and critical business behavior without requiring manual intervention on every release.

**Flow 2 — API: Insufficient Balance**

This flow was prioritized because it validates a critical business rule directly at the API level: a user must not be able to place a bet when the stake exceeds their available balance.

### What was intentionally left as manual

I would keep visual/UI validation, exploratory testing, and usability-related scenarios manual. These tests benefit from human judgment and are less valuable to automate when the expected result depends on visual presentation or subjective evaluation.

I would also keep low-frequency or highly variable scenarios manual initially, while the product requirements and business rules are still evolving. Automating unstable requirements can create maintenance overhead without providing proportional value.

### Top recommendations if the project scales

1. **CI/CD and test environment**

   Integrate the automated suites into a CI/CD pipeline. The pipeline should be able to build and run a dedicated test environment, including the web application in **headless mode**, so UI tests can execute consistently without requiring a local browser session.

2. **Layering, abstraction and project separation**

   Separate the automation into different projects/layers, for example **UI and API**, with clear abstraction levels and responsibilities. Common functionality should be reused through shared components rather than duplicated between tests.

   For the data model, I would introduce reusable structures such as:

   * `Matchup(home, away)`
   * `Fixture(matchup, league, date, odds)`

   This would make test data more readable, maintainable, and easier to extend as the application grows.

3. **Test data strategy and security**

   Introduce controlled and isolated test data, with mechanisms to create or reset users, balances, fixtures, and bets. Where possible, reuse the user IDs inherited from the existing projects rather than hardcoding them throughout the tests.

   Additionally, the test environment should have **authentication/login protection** rather than exposing the application or test endpoints without authentication.

4. **Clarify and formalize business rules and API contracts**

   Define explicit specifications for critical business rules and ensure that the API behavior matches the documented contracts.

   In this assessment, some requirements were ambiguous or inconsistent with the actual implementation. The specifications stated that only **upcoming matches** should be displayed, but matches from previous dates were also present. While this could be considered a bug, both types of events had **“Past”** or **“Upcoming”** labels, which were not defined in the specifications. The expected behavior and meaning of these labels should therefore be explicitly documented.

   Finally, currency representation should be standardized. The same balance/amount was displayed as **USD in some places and EUR in others**, so the expected currency and formatting should be explicitly defined and consistently applied across the UI and APIs.
