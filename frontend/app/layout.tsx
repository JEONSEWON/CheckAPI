import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { Toaster } from "react-hot-toast";
import { Providers } from "./providers";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "checkapi.io | Simple API Monitoring by Axiom Technologies",
  description: "Professional API uptime monitoring and public status pages. A core technology by Axiom Technologies for solo founders and engineering teams. Free tier available.",
  keywords: ["API monitoring", "uptime monitoring", "website monitoring", "health check", "API alerts", "downtime alerts"],
  authors: [{ name: "Axiom Technologies" }],
  creator: "Axiom Technologies",
  publisher: "Axiom Technologies",
  metadataBase: new URL("https://checkapi.io"),
  alternates: { canonical: "/" },
  verification: { google: "aPu3HfP0HcYJs4r-_azPdbeT1x8q_bLvWzHqoe_xay4" },
  openGraph: {
    type: "website",
    locale: "en_US",
    url: "https://checkapi.io",
    title: "checkapi.io | Simple API Monitoring by Axiom Technologies",
    description: "Professional API uptime monitoring and public status pages. A core technology by Axiom Technologies.",
    siteName: "CheckAPI by Axiom Technologies",
    images: [{ url: "/android-chrome-512x512.png", width: 512, height: 512, alt: "CheckAPI Logo" }],
  },
  twitter: {
    card: "summary_large_image",
    title: "checkapi.io | Simple API Monitoring by Axiom Technologies",
    description: "Professional API uptime monitoring and public status pages. Free tier available.",
    images: ["/android-chrome-512x512.png"],
    creator: "@imwon_dev",
  },
  icons: {
    icon: [
      { url: "/favicon-16x16.png", sizes: "16x16", type: "image/png" },
      { url: "/favicon-32x32.png", sizes: "32x32", type: "image/png" },
      { url: "/favicon-96x96.png", sizes: "96x96", type: "image/png" },
    ],
    shortcut: "/favicon.ico",
    apple: "/apple-touch-icon.png",
  },
  manifest: "/site.webmanifest",
};

export default function RootLayout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={inter.className}>
        <Providers>
          {children}
          <Toaster position="top-right" />
        </Providers>
      </body>
    </html>
  );
}
