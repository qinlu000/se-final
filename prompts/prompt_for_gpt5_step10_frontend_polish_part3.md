# Prompt for GPT-5: Frontend Polish Part 3 (Final Pages)

## Context
We are finalizing the **Neubrutalism ("Playful Pop")** redesign.
We discovered two pages that still rely on the old "Soft UI" style:
1.  Mini Program Login Page (`login.vue`)
2.  Admin Web Stats Page (`Stats.vue`)

**Reference**: `docs/ui_ux_design.md`

## Objective
Update these remaining files to strictly follow the Playful Pop aesthetic (Thick borders, Hard Shadows, Vibrant Solids).

## Step-by-Step Instructions

### 1. Mini Program Login Page
**Target File**: `mini-program/pages/login/login.vue`
*   **Card**: Replace the soft shadow container with a `.neu-card` (White bg, `2px black border`, `8px black shadow`).
*   **Inputs**:
    *   Remove grey background.
    *   Use white background with `2px solid black` border.
    *   Focus state: `background-color: #FFE600` (Yellow).
*   **Button**:
    *   Replace green background with **Electric Yellow** (`#FFE600`).
    *   Add `2px solid black` border and `4px` hard shadow.
    *   Text color: Black (`#000`), Bold.
*   **Background**: Ensure the page background uses the dotted pattern (`radial-gradient`).

### 2. Admin Web Stats Page
**Target File**: `admin-web/src/views/Stats.vue`
*   **Stat Cards**:
    *   **REMOVE** the linear gradients (`gradient-1`, `gradient-2`, etc.).
    *   Use **Solid Colors** for each card background:
        *   Card 1 (Users): Electric Yellow (`#FFE600`)
        *   Card 2 (Posts): Hot Pink (`#FF6B6B`)
        *   Card 3 (Active): Cyan (`#00F0FF`)
        *   Card 4 (Interactions): Purple (`#9D4EDD`)
    *   Add `2px solid black` border and `4px` hard shadow to each card.
    *   make text black (since backgrounds are bright).
*   **Charts (ECharts)**:
    *   **Line Chart**: Change line color to Black (`#000`). Remove area gradient (or make it a solid hatching pattern if possible, otherwise just transparent).
    *   **Pie Chart**: Add `2px black border` to pie slices. Use the palette colors (Yellow, Pink, Cyan, Purple).
    *   **Container**: Add `2px solid black` border and hard shadow to the chart containers.

## Constraints
*   **Consistency**: Reuse the CSS variables defined in previous steps where possible.
*   **Functionality**: Do not break the login logic or statistics fetching.

## Deliverables
*   `mini-program/pages/login/login.vue`
*   `admin-web/src/views/Stats.vue`
