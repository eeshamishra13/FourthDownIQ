/* =========================================================
   FOURTHDOWNIQ
   Frontend Interactions + ML API + Simulator + History
========================================================= */


/* =========================================================
   API
========================================================= */

const API_URL =
    "http://127.0.0.1:8000/predict";


/* =========================================================
   DOM HELPERS
========================================================= */

const $ = (id) =>
    document.getElementById(id);

const cursorGlow =
    document.querySelector(".cursor-glow");


/* =========================================================
   CURSOR GLOW
========================================================= */

document.addEventListener(
    "mousemove",
    (event) => {

        if (!cursorGlow) return;

        cursorGlow.style.left =
            `${event.clientX}px`;

        cursorGlow.style.top =
            `${event.clientY}px`;

    }
);


/* =========================================================
   THEME
========================================================= */

const themeToggle =
    $("themeToggle");

const savedTheme =
    localStorage.getItem(
        "fourthdowniq-theme"
    );

if (savedTheme === "dark") {

    document.body.classList.add("dark");

}


themeToggle?.addEventListener(
    "click",
    () => {

        document.body.classList.toggle("dark");

        const theme =
            document.body.classList.contains("dark")
                ? "dark"
                : "light";

        localStorage.setItem(
            "fourthdowniq-theme",
            theme
        );

    }
);


/* =========================================================
   MOBILE MENU
========================================================= */

const mobileMenuButton =
    $("mobileMenuButton");

const mobileMenu =
    $("mobileMenu");


mobileMenuButton?.addEventListener(
    "click",
    () => {

        mobileMenu?.classList.toggle(
            "open"
        );

    }
);


document
    .querySelectorAll(".mobile-menu a")
    .forEach(
        (link) => {

            link.addEventListener(
                "click",
                () => {

                    mobileMenu?.classList.remove(
                        "open"
                    );

                }
            );

        }
    );


/* =========================================================
   SCROLL REVEAL
========================================================= */

const revealElements =
    document.querySelectorAll(
        ".reveal"
    );


if ("IntersectionObserver" in window) {

    const revealObserver =
        new IntersectionObserver(
            (entries) => {

                entries.forEach(
                    (entry) => {

                        if (
                            entry.isIntersecting
                        ) {

                            entry.target.classList.add(
                                "visible"
                            );

                            revealObserver.unobserve(
                                entry.target
                            );

                        }

                    }
                );

            },
            {
                threshold: 0.10
            }
        );


    revealElements.forEach(
        (element) => {

            revealObserver.observe(
                element
            );

        }
    );

} else {

    revealElements.forEach(
        (element) => {

            element.classList.add(
                "visible"
            );

        }
    );

}


/* =========================================================
   STAGGER
========================================================= */

document
    .querySelectorAll(".metrics-grid .reveal")
    .forEach(
        (element, index) => {

            element.style.transitionDelay =
                `${index * 80}ms`;

        }
    );


document
    .querySelectorAll(".factor-grid .reveal")
    .forEach(
        (element, index) => {

            element.style.transitionDelay =
                `${index * 70}ms`;

        }
    );


/* =========================================================
   NAVBAR SCROLL
========================================================= */

const navbar =
    document.querySelector(".navbar");


window.addEventListener(
    "scroll",
    () => {

        if (!navbar) return;

        navbar.style.boxShadow =
            window.scrollY > 30
                ? "0 15px 50px rgba(0,0,0,.08)"
                : "none";

    },
    {
        passive: true
    }
);


/* =========================================================
   BUTTON FEEDBACK
========================================================= */

document
    .querySelectorAll(
        ".primary-button, .nav-button"
    )
    .forEach(
        (button) => {

            button.addEventListener(
                "click",
                () => {

                    button.style.transform =
                        "scale(.98)";

                    setTimeout(
                        () => {

                            button.style.transform =
                                "";

                        },
                        120
                    );

                }
            );

        }
    );


/* =========================================================
   ANALYZER ELEMENTS
========================================================= */

const analyzeButton =
    $("analyzeButton");

const resetButton =
    $("resetButton");

const analysisStatus =
    $("analysisStatus");

const resultStatus =
    $("resultStatus");

const resultCard =
    $("resultCard");


/* =========================================================
   INPUT HELPERS
========================================================= */

function getAnalyzerInput(id) {

    return $(id);

}


function getAnalyzerValues() {

    return {

        ydstogo:
            Number(
                $("ydstogo")?.value
            ),

        yardline:
            Number(
                $("yardline")?.value
            ),

        scoreDifferential:
            Number(
                $("scoreDifferential")?.value
            ),

        gameTime:
            Number(
                $("gameTime")?.value
            ),

        distanceGroup:
            $("distanceGroup")?.value || "",

        fieldZone:
            $("fieldZone")?.value || "",

        scoreState:
            $("scoreState")?.value || "",

        timeState:
            $("timeState")?.value || ""

    };

}


/* =========================================================
   TIME FORMAT
========================================================= */

function formatGameTime(seconds) {

    const totalSeconds =
        Math.max(
            0,
            Math.floor(
                Number(seconds) || 0
            )
        );

    const minutes =
        Math.floor(
            totalSeconds / 60
        );

    const remainingSeconds =
        totalSeconds % 60;

    return `${String(minutes).padStart(2,"0")}:${String(
        remainingSeconds
    ).padStart(2,"0")}`;

}


function updateTimeDisplay() {

    const gameTime =
        $("gameTime");

    if (!gameTime) return;

    const formatted =
        formatGameTime(
            gameTime.value
        );

    const display =
        $("gameTimeDisplay");

    if (display) {

        display.textContent =
            formatted;

    }

}


$("gameTime")?.addEventListener(
    "input",
    updateTimeDisplay
);


/* =========================================================
   VALIDATION
========================================================= */

function validateAnalyzerInputs() {

    const values =
        getAnalyzerValues();


    if (
        !Number.isFinite(values.ydstogo) ||
        !Number.isFinite(values.yardline) ||
        !Number.isFinite(values.scoreDifferential) ||
        !Number.isFinite(values.gameTime)
    ) {

        return "Please enter valid numeric values.";

    }


    if (
        values.ydstogo < 1 ||
        values.ydstogo > 99
    ) {

        return "Yards to go must be between 1 and 99.";

    }


    if (
        values.yardline < 1 ||
        values.yardline > 99
    ) {

        return "Yard line must be between 1 and 99.";

    }


    if (
        values.scoreDifferential < -50 ||
        values.scoreDifferential > 50
    ) {

        return "Score differential must be between -50 and 50.";

    }


    if (
        values.gameTime < 0 ||
        values.gameTime > 3600
    ) {

        return "Time remaining must be between 0 and 3600 seconds.";

    }


    if (!values.distanceGroup) {

        return "Please choose a distance group.";

    }


    if (!values.fieldZone) {

        return "Please choose a field zone.";

    }


    if (!values.scoreState) {

        return "Please choose a score state.";

    }


    if (!values.timeState) {

        return "Please choose a time state.";

    }


    return null;

}


/* =========================================================
   LOADING
========================================================= */

function setLoadingState(loading) {

    if (!analyzeButton) return;


    if (loading) {

        analyzeButton.disabled = true;

        analyzeButton.classList.add(
            "analyzing"
        );

        analyzeButton.dataset.originalText =
            analyzeButton.innerHTML;

        analyzeButton.innerHTML = `
            <span class="loading-spinner"></span>
            <span>Analyzing...</span>
        `;

    } else {

        analyzeButton.disabled = false;

        analyzeButton.classList.remove(
            "analyzing"
        );

        analyzeButton.innerHTML =
            analyzeButton.dataset.originalText ||
            `Analyze Situation <span>→</span>`;

    }

}


/* =========================================================
   RESET RESULT
========================================================= */

function resetPredictionOnly() {

    const recommendation =
        $("recommendation");

    const confidence =
        $("confidence");


    if (recommendation)
        recommendation.textContent = "—";

    if (confidence)
        confidence.textContent = "—";


    [
        "puntProbability",
        "fieldGoalProbability",
        "goProbability"
    ].forEach(
        (id) => {

            const element = $(id);

            if (element)
                element.textContent = "—";

        }
    );


    [
        "puntBar",
        "fieldGoalBar",
        "goBar"
    ].forEach(
        (id) => {

            const element = $(id);

            if (element) {

                element.style.setProperty(
                    "--width",
                    "0%"
                );

            }

        }
    );


    if (resultCard) {

        resultCard.classList.remove(
            "prediction-ready",
            "prediction-error",
            "prediction-analyzing"
        );

    }


    if ($("modelFactorsList")) {

        $("modelFactorsList").innerHTML = `
            <p>
                Model factors will appear after analysis.
            </p>
        `;

    }


    if ($("explanationList")) {

        $("explanationList").innerHTML = `
            <p>
                Enter a game situation and run the
                analysis to see the model reasoning.
            </p>
        `;

    }


    if ($("insightExplanation")) {

        $("insightExplanation").innerHTML = `
            <p>
                The model explanation will appear here
                after an analysis.
            </p>
        `;

    }


    if ($("insightConfidence"))
        $("insightConfidence").textContent = "0.00";


    if ($("insightSummary"))
        $("insightSummary").textContent =
            "Run an analysis to see the model's strategic signal.";


    for (let i = 1; i <= 6; i++) {

        const name =
            $(`insightFactor${i}Name`);

        const value =
            $(`insightFactor${i}Value`);

        const bar =
            $(`insightFactor${i}Bar`);


        if (name)
            name.textContent = "—";

        if (value)
            value.textContent = "—";

        if (bar) {

            bar.style.setProperty(
                "--width",
                "0%"
            );

            bar.parentElement?.classList.remove(
                "negative"
            );

        }

    }

}


/* =========================================================
   REQUEST PAYLOAD
========================================================= */

function createRequestData(values) {

    return {

        ydstogo:
            values.ydstogo,

        yardline_100:
            values.yardline,

        score_differential:
            values.scoreDifferential,

        game_seconds_remaining:
            values.gameTime,

        distance_group:
            values.distanceGroup,

        field_zone:
            values.fieldZone,

        score_state:
            values.scoreState,

        time_state:
            values.timeState

    };

}


/* =========================================================
   API CALL
========================================================= */

async function requestPrediction(values) {

    const requestData =
        createRequestData(values);


    const response =
        await fetch(
            API_URL,
            {

                method: "POST",

                headers: {

                    "Content-Type":
                        "application/json",

                    "Accept":
                        "application/json"

                },

                body:
                    JSON.stringify(
                        requestData
                    )

            }
        );


    if (!response.ok) {

        const errorText =
            await response.text();

        throw new Error(
            `API returned ${response.status}: ${errorText}`
        );

    }


    return await response.json();

}


/* =========================================================
   UPDATE MAIN RESULT
========================================================= */

function updatePredictionUI(result) {

    const recommendation =
        $("recommendation");


    const confidence =
        Number(
            result.confidence || 0
        );


    if (recommendation) {

        recommendation.textContent =
            result.recommended_decision ||
            "—";

    }


    if ($("confidence")) {

        $("confidence").textContent =
            `${confidence.toFixed(2)}%`;

    }


    const probabilities =
        result.probabilities || {};


    const punt =
        Number(
            probabilities.PUNT || 0
        );

    const fieldGoal =
        Number(
            probabilities.FIELD_GOAL || 0
        );

    const go =
        Number(
            probabilities.GO || 0
        );


    setProbability(
        "puntProbability",
        "puntBar",
        punt
    );


    setProbability(
        "fieldGoalProbability",
        "fieldGoalBar",
        fieldGoal
    );


    setProbability(
        "goProbability",
        "goBar",
        go
    );


    updateExplanation(
        result
    );


    updateModelFactors(
        result.model_factors
    );


    updateInsightsUI(
        result
    );


    if (resultCard) {

        resultCard.classList.remove(
            "prediction-analyzing",
            "prediction-error"
        );

        resultCard.classList.add(
            "prediction-ready"
        );

    }

}


/* =========================================================
   PROBABILITY
========================================================= */

function setProbability(
    textId,
    barId,
    value
) {

    const text =
        $(textId);

    const bar =
        $(barId);


    if (text) {

        text.textContent =
            `${value.toFixed(2)}%`;

    }


    requestAnimationFrame(
        () => {

            if (bar) {

                bar.style.setProperty(
                    "--width",
                    `${Math.min(value,100)}%`
                );

            }

        }
    );

}


/* =========================================================
   EXPLANATION
========================================================= */

function updateExplanation(result) {

    const explanationList =
        $("explanationList");

    const insightExplanation =
        $("insightExplanation");


    if (
        !Array.isArray(
            result.human_explanation
        )
    ) {

        return;

    }


    if (explanationList) {

        explanationList.innerHTML = "";

        result.human_explanation.forEach(
            (reason) => {

                const p =
                    document.createElement("p");

                p.textContent =
                    reason;

                explanationList.appendChild(
                    p
                );

            }
        );

    }


    if (insightExplanation) {

        insightExplanation.innerHTML = "";

        result.human_explanation.forEach(
            (reason) => {

                const p =
                    document.createElement("p");

                p.textContent =
                    reason;

                insightExplanation.appendChild(
                    p
                );

            }
        );

    }

}


/* =========================================================
   MODEL FACTORS
========================================================= */

function updateModelFactors(factors) {

    const list =
        $("modelFactorsList");


    if (
        !list ||
        !Array.isArray(factors)
    ) {

        return;

    }


    list.innerHTML = "";


    factors
        .slice(0,6)
        .forEach(
            (factor) => {

                const p =
                    document.createElement("p");

                const arrow =
                    document.createElement("span");

                const impact =
                    Number(
                        factor.impact || 0
                    );


                arrow.textContent =
                    factor.direction === "supports"
                        ? "↑"
                        : "↓";


                const feature =
                    document.createTextNode(
                        `${factor.feature} `
                    );


                const strong =
                    document.createElement("strong");


                strong.textContent =
                    impact.toFixed(3);


                p.appendChild(arrow);
                p.appendChild(feature);
                p.appendChild(strong);

                list.appendChild(p);

            }
        );

}


/* =========================================================
   INSIGHTS
========================================================= */

function updateInsightsUI(result) {

    const factors =
        Array.isArray(
            result.model_factors
        )
            ? result.model_factors
            : [];


    const confidence =
        Number(
            result.confidence || 0
        );


    if ($("insightConfidence")) {

        $("insightConfidence").textContent =
            confidence.toFixed(2);

    }


    if (
        $("insightSummary") &&
        result.recommended_decision
    ) {

        $("insightSummary").textContent =
            `The model recommends ${result.recommended_decision} with ${confidence.toFixed(2)}% confidence based on the current game situation.`;

    }


    const slots = [
        1,2,3,4,5,6
    ];


    const sorted =
        [...factors].sort(
            (a,b) =>
                Math.abs(
                    Number(b.impact || 0)
                ) -
                Math.abs(
                    Number(a.impact || 0)
                )
        );


    slots.forEach(
        (number,index) => {

            const factor =
                sorted[index];


            const name =
                $(`insightFactor${number}Name`);

            const value =
                $(`insightFactor${number}Value`);

            const bar =
                $(`insightFactor${number}Bar`);


            if (!factor) {

                if (name)
                    name.textContent = "—";

                if (value)
                    value.textContent = "—";

                if (bar)
                    bar.style.setProperty(
                        "--width",
                        "0%"
                    );

                return;

            }


            const impact =
                Number(
                    factor.impact || 0
                );


            if (name)
                name.textContent =
                    factor.feature;


            if (value) {

                const sign =
                    factor.direction === "supports"
                        ? "+"
                        : "−";

                value.textContent =
                    `${sign}${Math.abs(impact).toFixed(3)}`;

            }


            if (bar) {

                const percentage =
                    Math.min(
                        Math.abs(impact) * 220,
                        100
                    );


                requestAnimationFrame(
                    () => {

                        bar.style.setProperty(
                            "--width",
                            `${percentage}%`
                        );

                    }
                );


                bar.parentElement?.classList.toggle(
                    "negative",
                    factor.direction === "opposes"
                );

            }

        }
    );

}


/* =========================================================
   ANALYSIS HISTORY
========================================================= */

const HISTORY_KEY =
    "fourthdowniq-history";


function getHistory() {

    try {

        return JSON.parse(
            localStorage.getItem(
                HISTORY_KEY
            ) || "[]"
        );

    } catch {

        return [];

    }

}


function saveHistory(values,result) {

    const history =
        getHistory();


    const probabilities =
        result.probabilities || {};


    const item = {

        id:
            Date.now(),

        createdAt:
            new Date().toLocaleString(),

        ydstogo:
            values.ydstogo,

        yardline:
            values.yardline,

        scoreDifferential:
            values.scoreDifferential,

        gameTime:
            values.gameTime,

        recommendation:
            result.recommended_decision || "—",

        confidence:
            Number(
                result.confidence || 0
            ),

        probabilities

    };


    history.unshift(item);


    localStorage.setItem(
        HISTORY_KEY,
        JSON.stringify(
            history.slice(0,10)
        )
    );


    renderHistory();

}


function renderHistory() {

    const list =
        $("historyList");


    if (!list) return;


    const history =
        getHistory();


    if (!history.length) {

        list.innerHTML = `
            <div class="empty-history">
                <span>NO ANALYSES YET</span>
                <p>
                    Your completed predictions will appear here.
                </p>
            </div>
        `;

        return;

    }


    list.innerHTML = "";


    history.forEach(
        (item) => {

            const row =
                document.createElement("div");

            row.className =
                "history-item";


            const main =
                document.createElement("div");

            main.className =
                "history-main";


            const title =
                document.createElement("strong");


            title.textContent =
                `4TH & ${item.ydstogo} · YARD ${item.yardline}`;


            const small =
                document.createElement("small");


            small.textContent =
                `${item.createdAt} · Score ${item.scoreDifferential >= 0 ? "+" : ""}${item.scoreDifferential} · ${formatGameTime(item.gameTime)}`;


            main.appendChild(title);
            main.appendChild(small);


            const decision =
                document.createElement("div");

            decision.className =
                "history-decision";

            decision.textContent =
                item.recommendation;


            const confidence =
                document.createElement("div");

            confidence.className =
                "history-confidence";

            confidence.textContent =
                `${item.confidence.toFixed(1)}%`;


            row.appendChild(main);
            row.appendChild(decision);
            row.appendChild(confidence);


            list.appendChild(row);

        }
    );

}


$("clearHistory")?.addEventListener(
    "click",
    () => {

        localStorage.removeItem(
            HISTORY_KEY
        );

        renderHistory();

    }
);


/* =========================================================
   MAIN ANALYZER
========================================================= */

analyzeButton?.addEventListener(
    "click",
    async () => {

        const validationError =
            validateAnalyzerInputs();


        if (validationError) {

            if (analysisStatus)
                analysisStatus.textContent =
                    validationError;

            if (resultStatus)
                resultStatus.textContent =
                    "CHECK INPUT";

            resultCard?.classList.add(
                "prediction-error"
            );

            return;

        }


        const values =
            getAnalyzerValues();


        if (analysisStatus)
            analysisStatus.textContent =
                "Analyzing game situation...";


        if (resultStatus)
            resultStatus.textContent =
                "ANALYZING";


        resultCard?.classList.add(
            "prediction-analyzing"
        );


        setLoadingState(true);


        try {

            console.log(
                "FourthDownIQ request:",
                createRequestData(values)
            );


            const result =
                await requestPrediction(
                    values
                );


            console.log(
                "FourthDownIQ prediction:",
                result
            );


            updatePredictionUI(
                result
            );


            saveHistory(
                values,
                result
            );


            if (analysisStatus)
                analysisStatus.textContent =
                    "Analysis complete";


            if (resultStatus)
                resultStatus.textContent =
                    "READY";


            resultCard?.classList.remove(
                "prediction-analyzing",
                "prediction-error"
            );


            resultCard?.classList.add(
                "prediction-ready"
            );


            setTimeout(
                () => {

                    resultCard?.scrollIntoView({
                        behavior: "smooth",
                        block: "center"
                    });

                },
                180
            );


        } catch (error) {

            console.error(
                "FourthDownIQ API Error:",
                error
            );


            if (analysisStatus)
                analysisStatus.textContent =
                    "Unable to connect to prediction API.";


            if (resultStatus)
                resultStatus.textContent =
                    "ERROR";


            resultCard?.classList.remove(
                "prediction-analyzing",
                "prediction-ready"
            );


            resultCard?.classList.add(
                "prediction-error"
            );

        } finally {

            setLoadingState(false);

        }

    }
);


/* =========================================================
   SCENARIO PRESETS
========================================================= */

const SCENARIO_PRESETS = {

    shortYardage: {

        ydstogo: 2,
        yardline: 45,
        scoreDifferential: 3,
        gameTime: 420,

        distanceGroup: "short",
        fieldZone: "midfield",
        scoreState: "winning",
        timeState: "normal"

    },


    fourthAndLong: {

        ydstogo: 8,
        yardline: 65,
        scoreDifferential: -3,
        gameTime: 300,

        distanceGroup: "long",
        fieldZone: "opponent",
        scoreState: "losing",
        timeState: "normal"

    },


    fieldGoalRange: {

        ydstogo: 4,
        yardline: 30,
        scoreDifferential: 1,
        gameTime: 120,

        distanceGroup: "medium",
        fieldZone: "red_zone",
        scoreState: "winning",
        timeState: "late"

    },


    twoMinuteDrill: {

        ydstogo: 6,
        yardline: 55,
        scoreDifferential: -4,
        gameTime: 110,

        distanceGroup: "medium",
        fieldZone: "opponent",
        scoreState: "losing",
        timeState: "critical"

    },


    goalLine: {

        ydstogo: 2,
        yardline: 5,
        scoreDifferential: -2,
        gameTime: 75,

        distanceGroup: "short",
        fieldZone: "red_zone",
        scoreState: "losing",
        timeState: "late"

    }

};


function applyScenarioPreset(preset) {

    if (!preset) return;


    const fields = {

        ydstogo:
            "ydstogo",

        yardline:
            "yardline",

        scoreDifferential:
            "scoreDifferential",

        gameTime:
            "gameTime",

        distanceGroup:
            "distanceGroup",

        fieldZone:
            "fieldZone",

        scoreState:
            "scoreState",

        timeState:
            "timeState"

    };


    Object.entries(fields)
        .forEach(
            ([key,id]) => {

                const element =
                    $(id);

                if (!element) return;

                element.value =
                    preset[key];

                element.dispatchEvent(
                    new Event(
                        "change",
                        {
                            bubbles:true
                        }
                    )
                );

            }
        );


    updateTimeDisplay();

    resetPredictionOnly();


    if (analysisStatus)
        analysisStatus.textContent =
            "Scenario loaded — ready for analysis";


    if (resultStatus)
        resultStatus.textContent =
            "READY";


    document
        .querySelectorAll(
            ".scenario-button"
        )
        .forEach(
            button => {

                button.classList.remove(
                    "active"
                );

            }
        );

}


document
    .querySelectorAll(
        "[data-scenario]"
    )
    .forEach(
        button => {

            button.addEventListener(
                "click",
                () => {

                    const key =
                        button.dataset.scenario;

                    applyScenarioPreset(
                        SCENARIO_PRESETS[key]
                    );

                    button.classList.add(
                        "active"
                    );


                    /* Copy preset into simulator */

                    syncAnalyzerToSimulator();

                }
            );

        }
    );


/* =========================================================
   SIMULATOR
========================================================= */

const simYds =
    $("simYds");

const simYardline =
    $("simYardline");

const simScore =
    $("simScore");

const simTime =
    $("simTime");

const simDistance =
    $("simDistance");

const simField =
    $("simField");

const runSimulation =
    $("runSimulation");


function updateSimulatorLabels() {

    if ($("simYdsValue"))
        $("simYdsValue").textContent =
            simYds?.value || "4";


    if ($("simYardlineValue"))
        $("simYardlineValue").textContent =
            simYardline?.value || "45";


    if ($("simScoreValue"))
        $("simScoreValue").textContent =
            simScore?.value || "0";


    if ($("simTimeValue"))
        $("simTimeValue").textContent =
            formatGameTime(
                simTime?.value || 0
            );

}


[
    simYds,
    simYardline,
    simScore,
    simTime
]
.forEach(
    input => {

        input?.addEventListener(
            "input",
            updateSimulatorLabels
        );

    }
);


function syncAnalyzerToSimulator() {

    if (simYds)
        simYds.value =
            $("ydstogo")?.value || 4;


    if (simYardline)
        simYardline.value =
            $("yardline")?.value || 45;


    if (simScore)
        simScore.value =
            $("scoreDifferential")?.value || 0;


    if (simTime)
        simTime.value =
            $("gameTime")?.value || 300;


    if (simDistance)
        simDistance.value =
            $("distanceGroup")?.value ||
            "medium";


    if (simField)
        simField.value =
            $("fieldZone")?.value ||
            "midfield";


    updateSimulatorLabels();

}


function getSimulatorValues() {

    const yds =
        Number(
            simYds?.value || 4
        );

    const yardline =
        Number(
            simYardline?.value || 45
        );

    const score =
        Number(
            simScore?.value || 0
        );

    const time =
        Number(
            simTime?.value || 300
        );


    let distance =
        simDistance?.value ||
        "medium";


    let field =
        simField?.value ||
        "midfield";


    let scoreState =
        score > 0
            ? "winning"
            : score < 0
                ? "losing"
                : "tied";


    let timeState =
        time <= 120
            ? "critical"
            : time <= 300
                ? "late"
                : "normal";


    return {

        ydstogo: yds,

        yardline: yardline,

        scoreDifferential: score,

        gameTime: time,

        distanceGroup: distance,

        fieldZone: field,

        scoreState: scoreState,

        timeState: timeState

    };

}


function resetSimulationOutput() {

    if ($("simulationDecision"))
        $("simulationDecision").textContent =
            "Waiting";


    if ($("simulationConfidence"))
        $("simulationConfidence").textContent =
            "—";


    [
        ["simGo","simGoBar"],
        ["simFg","simFgBar"],
        ["simPunt","simPuntBar"]
    ]
    .forEach(
        ([text,bar]) => {

            if ($(text))
                $(text).textContent = "—";

            if ($(bar))
                $(bar).style.setProperty(
                    "--width",
                    "0%"
                );

        }
    );


    document
        .querySelectorAll(
            ".decision-card"
        )
        .forEach(
            card => {

                card.classList.remove(
                    "active"
                );

            }
        );


    if ($("simulationExplanation"))
        $("simulationExplanation").textContent =
            "Run a simulation to see how the decision changes.";

}


function updateSimulationOutput(result) {

    const probabilities =
        result.probabilities || {};


    const go =
        Number(
            probabilities.GO || 0
        );

    const fieldGoal =
        Number(
            probabilities.FIELD_GOAL || 0
        );

    const punt =
        Number(
            probabilities.PUNT || 0
        );


    const confidence =
        Number(
            result.confidence || 0
        );


    if ($("simulationDecision"))
        $("simulationDecision").textContent =
            result.recommended_decision ||
            "—";


    if ($("simulationConfidence"))
        $("simulationConfidence").textContent =
            `${confidence.toFixed(2)}%`;


    setSimulationProbability(
        "simGo",
        "simGoBar",
        go
    );


    setSimulationProbability(
        "simFg",
        "simFgBar",
        fieldGoal
    );


    setSimulationProbability(
        "simPunt",
        "simPuntBar",
        punt
    );


    const recommendation =
        String(
            result.recommended_decision ||
            ""
        ).toUpperCase();


    document
        .querySelectorAll(
            ".decision-card"
        )
        .forEach(
            card => {

                card.classList.toggle(
                    "active",
                    card.dataset.decision ===
                    normalizeDecision(
                        recommendation
                    )
                );

            }
        );


    if (
        $("simulationExplanation") &&
        Array.isArray(
            result.human_explanation
        )
    ) {

        $("simulationExplanation").textContent =
            result.human_explanation[0] ||
            `The model recommends ${result.recommended_decision}.`;

    }

}


function normalizeDecision(decision) {

    if (
        decision.includes("FIELD") ||
        decision.includes("KICK")
    ) {

        return "FIELD_GOAL";

    }


    if (
        decision.includes("PUNT")
    ) {

        return "PUNT";

    }


    return "GO";

}


function setSimulationProbability(
    textId,
    barId,
    value
) {

    if ($(textId))
        $(textId).textContent =
            `${value.toFixed(1)}%`;


    requestAnimationFrame(
        () => {

            if ($(barId))
                $(barId).style.setProperty(
                    "--width",
                    `${Math.min(value,100)}%`
                );

        }
    );

}


runSimulation?.addEventListener(
    "click",
    async () => {

        const values =
            getSimulatorValues();


        runSimulation.disabled = true;

        const original =
            runSimulation.innerHTML;


        runSimulation.innerHTML = `
            <span class="loading-spinner"></span>
            <span>Simulating...</span>
        `;


        try {

            const result =
                await requestPrediction(
                    values
                );


            updateSimulationOutput(
                result
            );


        } catch (error) {

            console.error(
                "Simulation error:",
                error
            );


            if ($("simulationDecision"))
                $("simulationDecision").textContent =
                    "API Error";


            if ($("simulationExplanation"))
                $("simulationExplanation").textContent =
                    "The simulator could not reach the prediction API. Make sure FastAPI is running.";

        } finally {

            runSimulation.disabled =
                false;

            runSimulation.innerHTML =
                original;

        }

    }
);


/* =========================================================
   BACKEND TESTING
   =========================================================

   We intentionally test the real /predict endpoint rather
   than inventing a /health endpoint that may not exist.
========================================================= */

async function testBackendConnection() {

    const testSituation = {

        ydstogo: 4,

        yardline_100: 45,

        score_differential: 0,

        game_seconds_remaining: 300,

        distance_group: "medium",

        field_zone: "midfield",

        score_state: "tied",

        time_state: "normal"

    };


    try {

        const response =
            await fetch(
                API_URL,
                {

                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json",
                        "Accept":
                            "application/json"
                    },

                    body:
                        JSON.stringify(
                            testSituation
                        )

                }
            );


        if (!response.ok) {

            throw new Error(
                `Backend returned ${response.status}`
            );

        }


        const result =
            await response.json();


        console.log(
            "FourthDownIQ backend test passed:",
            result
        );


        return true;

    } catch (error) {

        console.error(
            "FourthDownIQ backend test failed:",
            error
        );


        return false;

    }

}


/* =========================================================
   RESET ANALYZER
========================================================= */

resetButton?.addEventListener(
    "click",
    () => {

        [
            "ydstogo",
            "yardline",
            "scoreDifferential",
            "gameTime"
        ]
        .forEach(
            id => {

                if ($(id))
                    $(id).value = "";

            }
        );


        [
            "distanceGroup",
            "fieldZone",
            "scoreState",
            "timeState"
        ]
        .forEach(
            id => {

                if ($(id))
                    $(id).selectedIndex = 0;

            }
        );


        updateTimeDisplay();

        resetPredictionOnly();


        if (analysisStatus)
            analysisStatus.textContent =
                "Ready for analysis";


        if (resultStatus)
            resultStatus.textContent =
                "READY";


        document
            .querySelectorAll(
                ".scenario-button"
            )
            .forEach(
                button => {

                    button.classList.remove(
                        "active"
                    );

                }
            );

    }
);


/* =========================================================
   KEYBOARD SHORTCUTS
========================================================= */

document.addEventListener(
    "keydown",
    (event) => {

        if (
            (event.ctrlKey ||
                event.metaKey) &&
            event.key === "Enter"
        ) {

            event.preventDefault();

            if (
                analyzeButton &&
                !analyzeButton.disabled
            ) {

                analyzeButton.click();

            }

        }


        if (
            event.key === "Escape"
        ) {

            const active =
                document.activeElement;


            if (
                active &&
                (
                    active.tagName === "INPUT" ||
                    active.tagName === "SELECT"
                )
            ) {

                return;

            }


            resetButton?.click();

        }

    }
);


/* =========================================================
   INITIALIZE
========================================================= */

updateTimeDisplay();

updateSimulatorLabels();

renderHistory();


/*
 * Sync simulator with default analyzer state.
 */

syncAnalyzerToSimulator();


/*
 * Backend connectivity check.
 *
 * This does not block the UI.
 */

testBackendConnection();


/* =========================================================
   END OF FOURTHDOWNIQ
========================================================= */