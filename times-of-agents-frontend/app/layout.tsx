import type { Metadata } from "next";
import { playfair, inter } from "@/lib/fonts";
import Nav from "@/components/layout/Nav";
import BreakingBanner from "@/components/layout/BreakingBanner";
import "./globals.css";

export const metadata: Metadata = {
  title: "AgentPress",
  description: "AI-powered editorial newspaper",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className={`${playfair.variable} ${inter.variable}`}>
      <body className="font-inter bg-off-white text-charcoal antialiased">
        <Nav />
        <BreakingBanner />
        <main className="max-w-[1280px] mx-auto px-6 py-8 min-w-0">
          {children}
        </main>
      </body>
    </html>
  );
}
