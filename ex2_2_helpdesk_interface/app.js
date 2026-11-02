(() => {
  const form = document.querySelector("#request-form");
  const status = document.querySelector("#status");
  const summary = document.querySelector("#summary-details");
  const empty = document.querySelector("#summary-empty");
  const allowed = new Set(["Accounts", "Network", "Hardware", "Software", "Other"]);
  form.addEventListener("submit", (event) => {
    event.preventDefault();
    status.textContent = "";
    const data = new FormData(form);
    const category = String(data.get("category") || "");
    const title = String(data.get("title") || "").trim();
    const description = String(data.get("description") || "").trim();
    if (!allowed.has(category)) { status.textContent = "Choose a valid category."; form.elements.category.focus(); return; }
    if (title.length < 5 || title.length > 80) { status.textContent = "Title must be 5 to 80 characters."; form.elements.title.focus(); return; }
    if (description.length < 10 || description.length > 1000) { status.textContent = "Description must be 10 to 1,000 characters."; form.elements.description.focus(); return; }
    empty.hidden = true;
    summary.replaceChildren();
    const values = [["Category", category], ["Title", title], ["Description", description], ["Urgency", String(data.get("urgency"))], ["Preferred contact", String(data.get("contact"))]];
    for (const [label, value] of values) {
      const dt = document.createElement("dt"); dt.textContent = label;
      const dd = document.createElement("dd"); dd.textContent = value;
      summary.append(dt, dd);
    }
    summary.hidden = false;
    status.textContent = "Request details validated. This local demo did not send or save your request.";
  });
})();
