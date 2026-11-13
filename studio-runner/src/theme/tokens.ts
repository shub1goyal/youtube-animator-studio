import { loadFont as loadCinzel } from "@remotion/google-fonts/Cinzel";
import { loadFont as loadInstrumentSerif } from "@remotion/google-fonts/InstrumentSerif";
import { loadFont as loadSpaceGrotesk } from "@remotion/google-fonts/SpaceGrotesk";
import { loadFont as loadJetBrainsMono } from "@remotion/google-fonts/JetBrainsMono";
import { addCollection } from "@iconify/react";
import gameIcons from "@iconify-json/game-icons/icons.json";
import lucideIcons from "@iconify-json/lucide/icons.json";

// Register 5,500+ artist-drawn vector icons offline so zero network requests ever occur during render
addCollection(gameIcons);
addCollection(lucideIcons);

const cinzel = loadCinzel("normal", { weights: ["700", "900"], subsets: ["latin"] });
const instrumentSerif = loadInstrumentSerif("italic", { weights: ["400"], subsets: ["latin"] });
const spaceGrotesk = loadSpaceGrotesk("normal", { weights: ["500", "700"], subsets: ["latin"] });
const jetBrainsMono = loadJetBrainsMono("normal", { weights: ["600", "700"], subsets: ["latin"] });

export const FONTS = {
  display: cinzel.fontFamily,
  serifItalic: instrumentSerif.fontFamily,
  sans: spaceGrotesk.fontFamily,
  mono: jetBrainsMono.fontFamily,
};

export const COLORS = {
  parchmentCenter: "#FAF1DF",
  parchmentEdge: "#E4D2AF",
  parchmentCard: "#F5E9D0",
  seaFill: "#CEDAD6",
  seaDeep: "#BAC9C4",
  landFill: "#EDE0C4",
  landStroke: "#6E5F4B",
  ink: "#1A1613",
  inkSoft: "#4A4035",
  inkMuted: "#7C6E5D",
  gridLine: "rgba(58, 46, 33, 0.09)",
  rome: "#B82925",
  romeDark: "#7A1815",
  romeSoft: "rgba(184, 41, 37, 0.16)",
  carthage: "#1D4E78",
  carthageDark: "#11314D",
  carthageSoft: "rgba(29, 78, 120, 0.16)",
  gold: "#D4941E",
  goldBright: "#F2B735",
  obsidianCenter: "#1D1916",
  obsidianEdge: "#0E0C0A",
  chalk: "#F6EFE2",
};

export const SPRINGS = {
  snappy: { damping: 16, stiffness: 190, mass: 0.8 },
  heavy: { damping: 18, stiffness: 120, mass: 1.1 },
  bouncy: { damping: 12, stiffness: 170, mass: 0.75 },
  camera: { damping: 24, stiffness: 90, mass: 1.2 },
};
