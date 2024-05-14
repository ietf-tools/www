document.querySelector("html").addEventListener("click", (e) => {
    if (e.target.tagName == "A") {
        const href = e.target.getAttribute("href") || ""
        if (href.startsWith("https://www.ietf.org/mailman/listinfo/")) {
            wagtailAbTesting.triggerEvent("navigate-mailman")
        }
        if (href.startsWith("https://registration.ietf.org/")) {
            wagtailAbTesting.triggerEvent("navigate-registration")
        }
    }
})
