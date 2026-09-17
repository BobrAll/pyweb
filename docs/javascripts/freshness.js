(function () {
    var GREEN = [102, 187, 106, 0.40];
    var GRAY = [128, 128, 128, 0.08];
    var WINDOW_MS = 60000;
    var STEP_MS = 500;

    function blend(k) {
        var r = Math.round(GREEN[0] + (GRAY[0] - GREEN[0]) * k);
        var g = Math.round(GREEN[1] + (GRAY[1] - GREEN[1]) * k);
        var b = Math.round(GREEN[2] + (GRAY[2] - GREEN[2]) * k);
        var a = GREEN[3] + (GRAY[3] - GREEN[3]) * k;
        return "rgba(" + r + "," + g + "," + b + "," + a.toFixed(3) + ")";
    }

    function tick() {
        var now = Date.now();
        document.querySelectorAll(".fresh-box").forEach(function (box) {
            var ts = Date.parse(box.dataset.buildTs || "");
            if (isNaN(ts)) {
                return;
            }
            var k = (now - ts) / WINDOW_MS;
            var color = "";
            if (k < 1) {
                color = blend(Math.max(0, k));
            }
            box.querySelectorAll("table").forEach(function (table) {
                table.style.backgroundColor = color;
            });
        });
    }

    if (document.querySelector(".fresh-box")) {
        tick();
        setInterval(tick, STEP_MS);
    }
})();
