import { useState, useEffect } from "react";

// TODO: FIX ACTIVE FILTER
export default function Filters() {
  const filters = [
    "All Recipes",
    "Breakfast",
    "Lunch",
    "Dinner",
    "Vegetarian",
    "Vegan",
  ];

  const [activeFilter, setActiveFilter] = useState(filters[0]);

  useEffect(() => {
    console.log("Active filter updated:", activeFilter);
  }, [activeFilter]);

  const handleFilterClick = (filter: string) => {
    console.log("Clicked filter:", filter);
    console.log("Current state before update:", activeFilter);

    setActiveFilter(filter);

    console.log("Current state after update attempt:", activeFilter);
  };

  return (
    <div className="flex items-center gap-x-4 bg-gray-100 text-gray-600 py-1 mx-20 rounded-xl mb-6">
      {filters.map((filter, index) => (
        <div
          key={index}
          className={`cursor-pointer py-1 px-4 ml-2 rounded transition-colors 
            ${
              activeFilter === filter
                ? "bg-white text-black shadow-sm"
                : "hover:bg-white hover:text-black hover:shadow-sm"
            }`}
          onClick={() => handleFilterClick(filter)}
        >
          {filter}
        </div>
      ))}
    </div>
  );
}
