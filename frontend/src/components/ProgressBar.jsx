import { motion } from "framer-motion";

export default function ProgressBar({ value }) {
  return (
    <div className="w-full bg-gray-700 rounded-full h-3 overflow-hidden">
      <motion.div
        initial={{ width: 0 }}
        animate={{ width: `${value}%` }}
        transition={{ duration: 0.8, ease: "easeInOut" }}
        className={`h-3 ${
          value > 70
            ? "bg-green-500"
            : value > 40
            ? "bg-yellow-500"
            : "bg-red-500"
        }`}
      />
    </div>
  );
}
