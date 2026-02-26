import type { Metadata } from "next";
import { Poppins } from "next/font/google";
import "./globals.css";
import { VacantesProvider } from "@/context/VacantesContext";

// fuente principal más llamativa
const poppins = Poppins({
  weight: ["300", "400", "500", "600", "700", "800"],
  subsets: ["latin"],
  variable: "--font-sans",
});

export const metadata: Metadata = {
  title: "TrabajosWeb - Portal de Empleos",
  description: "Descubre las mejores oportunidades de trabajo en Ecuador",
  keywords: ["empleos", "vacantes", "trabajo", "Ecuador"],
  authors: [{ name: "TrabajosWeb" }],
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="es">
      <head />
      <body
        className={`${poppins.variable} antialiased flex flex-col min-h-screen`}
      >
        <VacantesProvider>
          {children}
          <footer className="mt-auto py-6 text-center text-sm text-slate-400 flex flex-col items-center gap-2">
            <div className="flex items-center gap-1">
              <span className="text-xs">© {new Date().getFullYear()}</span>
              <span className="mx-1">·</span>
              <span className="font-medium">Desarrollado por Danilo Pin</span>
            </div>
            <a
              href="https://www.linkedin.com/in/danilo-miguel-pin-veloz/"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-1 text-cyan-400 hover:text-cyan-300 transition-colors"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="16"
                height="16"
                fill="currentColor"
                viewBox="0 0 16 16"
              >
                <path d="M0 1.146C0 .513.324 0 .725 0h14.55c.4 0 .725.513.725 1.146v13.708c0 .633-.325 1.146-.725 1.146H.725A.723.723 0 010 14.854V1.146zm4.943 12.248V6.169H2.542v7.225h2.401zm-1.2-8.212c.837 0 1.358-.554 1.358-1.247-.015-.709-.521-1.246-1.343-1.246-.822 0-1.358.537-1.358 1.246 0 .693.521 1.247 1.328 1.247h.015zm4.908 8.212h2.4v-4.002c0-.214.015-.428.08-.579.177-.428.58-.872 1.257-.872.888 0 1.243.657 1.243 1.62v4.833h2.4V9.208c0-2.221-1.184-3.254-2.764-3.254-1.279 0-1.845.7-2.165 1.193h.03v-1.025h-2.4c.03.657 0 7.225 0 7.225z"/>
              </svg>
              <span>LinkedIn</span>
            </a>
          </footer>
        </VacantesProvider>
      </body>
    </html>
  );
}
