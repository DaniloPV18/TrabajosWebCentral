import { LABELS } from "@/constants/labels";
import { COLORS } from "@/constants/colors";

interface HeaderProps {
  totalVacantes: number;
}

export const Header = ({ totalVacantes }: HeaderProps) => {
  return (
    <header className={`${COLORS.bg.secondary} border-b ${COLORS.border.light} sticky top-0 z-40 backdrop-blur-xl bg-opacity-90 shadow-lg shadow-slate-950/50`}>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="flex items-center gap-4">
          <div className="text-6xl drop-shadow-2xl animate-pulse" style={{ animationDuration: "3s" }} aria-hidden="true">
            🕷️
          </div>
          <div className="flex-1">
            <h1 className={`text-5xl font-bold bg-gradient-to-r from-cyan-300 via-violet-400 to-pink-400 bg-clip-text text-transparent mb-1`}>
              {LABELS.TITULO_PORTAL}
            </h1>
            <p className={`text-sm ${COLORS.text.secondary} flex items-center gap-2`}>
              <span>{LABELS.SUBTITULO_PORTAL}</span>
              <span className="w-1 h-1 rounded-full bg-cyan-400"></span>
              <span className="text-cyan-400 font-semibold">{totalVacantes}</span>
              <span className="text-cyan-400">{LABELS.VACANTES}</span>
            </p>
          </div>
        </div>
      </div>
    </header>
  );
};
