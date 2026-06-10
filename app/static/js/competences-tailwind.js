tailwind.config = {
    darkMode: "class",
    theme: {
        extend: {
            colors: {
                primary: "#1a237e",
                secondary: "#00c853",
                "on-primary": "#ffffff",
                "on-secondary": "#ffffff",
                background: "#f9f9fb",
                surface: "#ffffff",
                "on-background": "#1a1c1d",
                "on-surface": "#1a1c1d",
                "outline-variant": "#e2e2e4",
                "surface-container-low": "#f3f3f5",
                "surface-container": "#eeeef0",
                "primary-container": "#e8eaf6",
                "on-primary-container": "#1a237e"
            },
            borderRadius: {
                DEFAULT: "0.5rem",
                lg: "1rem",
                xl: "1.5rem",
                full: "9999px"
            },
            fontFamily: {
                "body-md": ["Lora", "serif"],
                "headline-lg": ["Playfair Display", "serif"],
                "display-lg": ["Playfair Display", "serif"]
            },
            maxWidth: {
                "container-max": "1280px"
            }
        }
    }
};
