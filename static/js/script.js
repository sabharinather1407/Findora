/* =========================================================
   ACADEMIC BLOCK FIELD
========================================================= */

const locationType = document.getElementById("location-type");
const academicBlockGroup = document.getElementById("academic-block-group");
const locationDetails = document.getElementById("location-details");

if (locationType) {

    locationType.addEventListener("change", function () {

        if (this.value === "Academic Block") {

            if (academicBlockGroup) {
                academicBlockGroup.style.display = "flex";
            }

            if (locationDetails) {
                locationDetails.required = true;
            }

        } else {

            if (academicBlockGroup) {
                academicBlockGroup.style.display = "none";
            }

            if (locationDetails) {
                locationDetails.required = false;
                locationDetails.value = "";
            }

        }

    });

}


/* =========================================================
   DARK MODE
========================================================= */

const savedTheme = localStorage.getItem("refind-theme");

if (savedTheme === "dark") {

    document.documentElement.dataset.theme = "dark";

}


/* =========================================================
   CREATE DARK MODE BUTTON
========================================================= */

const navLinks = document.querySelector(".nav-links");

if (navLinks) {

    const themeButton = document.createElement("button");

    themeButton.type = "button";

    themeButton.className = "theme-toggle";

    themeButton.setAttribute(
        "aria-label",
        "Toggle dark mode"
    );


    function updateThemeButton() {

        if (
            document.documentElement.dataset.theme === "dark"
        ) {

            themeButton.textContent = "☀️";

            themeButton.title = "Switch to light mode";

        } else {

            themeButton.textContent = "🌙";

            themeButton.title = "Switch to dark mode";

        }

    }


    themeButton.addEventListener("click", function () {

        const isDark =
            document.documentElement.dataset.theme === "dark";


        if (isDark) {

            document.documentElement.removeAttribute("data-theme");

            localStorage.setItem(
                "refind-theme",
                "light"
            );

        } else {

            document.documentElement.dataset.theme = "dark";

            localStorage.setItem(
                "refind-theme",
                "dark"
            );

        }


        updateThemeButton();

    });


    navLinks.appendChild(themeButton);

    updateThemeButton();

}