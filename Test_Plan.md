# Single Bet Placement — Risk-Based Test Scenarios

## 1. cope

This test plan covers the Single Bet Placement functionality for the desktop web application.

### In scope

- Upcoming football/soccer matches
- Stake validation
- Available balance validation
- Bet placement
- Potential payout calculation
- Successful bet receipt
- Error handling during bet placement
- Match and selection consistency

### Out of scope

- Live betting
- Multi-bets / accumulators
- Other sports
- Mobile-specific UX requirements

## 2. Risk-Based Approach


The highest risks are concentrated on the placement of a bet and the consistency of the user's financial state.

The scenarios prioritized:
1. Successful placement of a valid bet.
2. Prevention of invalid or unaffordable bets.
3. Correct selection handling for the single-bet constraint.
4. Correct handling of placement failures and retries.

Lower-risk areas such as filters and additional UI checks are left for exploratory/regression coverage, due to assignment constraints.


## 3. Prioritized Test Scenarios

### TS-001 — Successfully place a valid single bet

**Priority:** Critical

**Risk Rationale:**  
This is the core business flow. Failure would prevent users from placing bets, while incorrect stake, odds, payout, or balance handling could result in financial inconsistencies.

**Preconditions:**

- User has a valid user id.
- At least one upcoming football match is available.
- User has sufficient balance.

**Steps:**

1. Open the application with a valid user ID.
2. Select a valid outcome for an upcoming football match. 
3. Verify that the selection appears in the bet slip.
4. Enter a valid stake, for example €10.00.
5. Verify the selected odds and potential payout.
6. Click **Place Bet**.
7. Wait for the placement operation to complete.
8. Review the success receipt.

**Expected Result:**

- The selected outcome appears in the bet slip.
- The stake is accepted.
- Potential payout is calculated as `stake × odds`.
- The Place Bet button enters the `Placing...` state.
- The bet is successfully placed.
- The stake is deducted from the available balance.
- A success receipt is displayed.
- The receipt contains Bet ID, match details, selection, stake, odds at placement, potential payout, and placement timestamp.
- Closing the receipt returns the user to the main flow without an active selection.

---

### TS-002 — Prevent placement when the stake exceeds the available balance

**Priority:** Critical

**Risk Rationale:**  
Allowing a user to place a bet for more than their available balance could result in an invalid financial transaction and inconsistent account state.

**Preconditions:**

- User has a valid user id.
- User available balance is within boundaries, excluding maximum.
- An upcoming football match is available.

**Steps:**

1. Open the application with a valid user ID.
2. Select a valid outcome for an upcoming football match. 
3. Enter a stake greater than the available balance.
4. Attempt to place the bet.

**Expected Result:**

- The application identifies that the stake exceeds the available balance.
- An `Insufficient balance` message is displayed.
- The **Place Bet** is disable.

---

### TS-003 — Validate stake boundaries and input rules

**Priority:** High

**Risk Rationale:**  
Stake validation directly protects the financial rules of the application. Incorrect boundary handling could allow invalid bets or reject valid ones.

**Preconditions:**

- User has a valid user id.
- A valid match and outcome are selected.
- The user has sufficient balance for the valid values being tested.

**Steps:**
1. Open the application with a valid user ID.
2. Select a valid outcome for an upcoming football match. 

Validate the following stake values:
3. €0.99
4. €1.00
5. €100.00
6. €100.01 
7. A value with more than two decimal places, e.g. €10.001
8. A non-numeric value
9. More than one decimal separator
10. An empty value


11. Attempt to proceed with bet placement where applicable.

**Expected Result:**

- Values below the configured minimum prevents bet placement.
- Values above €100.00 prevents bet placement.
- Values with more than two decimal places are rejected.
- Non-numeric values are rejected.
- An empty stake prevents bet placement.
- Valid values within the configured range are accepted.
- Appropriate validation feedback is displayed for non-valid values.

**Specification Note:**

The specification contains an inconsistency regarding the minimum stake:

- Business Rules state a minimum stake of €1.00.
- Validation Rules state €1.01 as the minimum positive value.
- The minimum-stake UI message states `Minimum stake is €1.00`.

The specification is inconsistent regarding the minimum stake (€1.00 vs. €1.01), potentially because the minimum odds value is €1.01, so the intended behavior should be clarified.

---

### TS-004 — Ensure only one selection can be active

**Priority:** High

**Risk Rationale:**  
The product supports only one active selection at a time. Incorrect selection handling could result in users placing a different bet than intended or accidentally creating multi-selection behavior.

**Preconditions:**

- User has a valid user id.
- At least one upcoming football match is available.

**Steps:**

1. Open the application with a valid user ID.
2. Select the **1** outcome of a match.
3. Verify that Home appears in the bet slip.
4. Select the **X** outcome for the same match. 
5. Verify the bet slip.
6. Select the **2** outcome for the same match.
7. Verify the bet slip.
8. If possible, select an outcome from another match.
9. Verify the bet slip again.

**Expected Result:**

- Only one selection is active at any time.
- Selecting a new odds button replaces the previous selection.
- The bet slip reflects only the latest selection.
- No accumulator/multi-bet is created.
- The stake is erased upon new selection.

---

### TS-005 — Handle failed placement and retry correctly

**Priority:** High

**Risk Rationale:**  
Bet placement is a state-changing operation. Failures must not leave the UI in an ambiguous state or incorrectly deduct funds. The retry flow must also avoid duplicate transactions.

**Preconditions:**

- User has a valid user id.
- A valid match, outcome, and stake are selected.
- A placement failure can be triggered or simulated.

**Steps:**

1. Open the application with a valid user ID.
2. Select a valid outcome for an upcoming football match. 
3. Enter a valid stake.
4. Trigger a placement failure.
5. Verify the error modal.
6. Click **Rebet**.
7. Observe the placement flow.
8. Repeat the scenario and select **Close**.
9. Repeat the scenario and close the modal using the top-right **X**.

**Expected Result:**

- The Place Bet button enters the `Placing...` state.
- A failed request results in the error modal.
- The modal title is **Something went wrong**.
- The modal explains that the bet could not be processed.
- **Rebet** closes the modal and retries placement.
- **Close** closes the modal and clears the current selection/stake.
- The top-right **X** has the same behavior as Close.
- A failed placement does not incorrectly deduct the stake.
- A successful retry results in a single successful bet and consistent balance.

---

### TS-006 — Reject invalid betting requests at API level

**Priority:** High

**Risk Rationale:**  
Client-side validation can be bypassed. The backend must independently enforce authentication, request format, match validity, selection validity, and stake rules to protect business and financial integrity.

**Preconditions:**

- API documentation is available through `/api/docs`.
- A valid user context and match are available.

**Steps:**

Using the API directly, send requests with:

1. Missing `x-user-id`.
2. Invalid `x-user-id`.
3. Missing `matchId`.
4. Blank `matchId`.
5. Unknown `matchId`.
6. Invalid selection value.
7. Missing selection.
8. Missing stake.
9. Non-numeric stake.
10. Malformed JSON.
11. Unsupported HTTP method.

**Expected Result:**

- Missing/invalid user context is rejected as unauthorized.
- Missing or blank match IDs are rejected.
- Unknown matches are rejected.
- Selection values other than `HOME`, `DRAW`, or `AWAY` are rejected.
- Missing or invalid stakes are rejected.
- Malformed request bodies are rejected.
- Unsupported methods return Method Not Allowed.
- Invalid requests do not create a successful bet or incorrectly modify the user's balance.

Expected error classes:

- `400` — malformed payload
- `401` — unauthorized user context
- `405` — method not allowed
- `409` — bet already in progress
- `422` — semantic validation failure
- `500` — unexpected server failure

## 4. Priority Summary

| ID | Scenario | Priority | Primary Risk |
|---|---|---|---|
| TS-001 | Successfully place a valid single bet | Critical | Core betting / financial transaction |
| TS-002 | Prevent placement when stake exceeds balance | Critical | Financial integrity |
| TS-003 | Validate stake boundaries and input rules | High | Invalid financial transactions |
| TS-004 | Ensure only one selection can be active | High | Incorrect bet selection |
| TS-005 | Handle failed placement and retry correctly | High | Inconsistent or duplicate transactions |
| TS-006 | Reject invalid betting requests at API level | High | Backend/business-rule bypass |

## 5. Exploratory Coverage

During execution, exploratory checks should focus on state and timing risks around the betting flow:

- Rapidly trigger **Place Bet** multiple times.
- Try to change the selection immediately before placement.
- Removing the selection while entering a stake.
- Using **Remove All** after entering a stake.
- Changing the page with an active selection.
- Closing a success receipt and verifying the bet slip state.
- Retrying after a failed placement.
- Verifying that displayed odds match the odds used for payout calculation.
- Verifying that the balance displayed in the header and bet slip remains consistent.
- Verifying that the receipt match, selection, stake, odds, and payout correspond to the placed bet.

