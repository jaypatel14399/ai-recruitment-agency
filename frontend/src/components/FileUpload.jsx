import React from "react";

export default function FileUpload({ label, multiple, onFileChange }) {
  const handleChange = (e) => {
    const files = Array.from(e.target.files);
    onFileChange(multiple ? files : files[0]);
  };

  return (
    <div>
      <label className="block mb-2 font-medium">{label}</label>
      <input
        type="file"
        multiple={multiple}
        onChange={handleChange}
        className="mb-4 border rounded w-full p-2"
      />
    </div>
  );
}