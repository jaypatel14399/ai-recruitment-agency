import { useState } from "react";
import FileUpload from "./components/FileUpload";

function App() {
  const [resumes, setResumes] = useState<File[]>([]);
  const [jobDescription, setJobDescription] = useState<File | null>(null);
  const [topMatches, setTopMatches] = useState<
    { filename: string; similarity: number }[]
  >([]);

  const handleSubmit = async () => {
    const formData = new FormData();
    resumes.forEach((file) => formData.append("resumes", file));
    if (jobDescription) {
      formData.append("job_description", jobDescription);
    }

  try {
    const res = await fetch("http://localhost:8000/upload-resumes", {
      method: "POST",
      body: formData,
    });

    if (!res.ok) {
      throw new Error(`Error: ${res.statusText}`);
    }

    const data = await res.json();
    console.log("Backend response:", data);
    setTopMatches(data.top_matches || []);
  } catch (err) {
    console.error("Upload failed:", err);
  }
};


  return (
    <div className="min-h-screen bg-gray-100 flex flex-col items-center justify-center p-8">
      <h1 className="text-3xl font-bold mb-8 text-gray-800">
        Recruitment AI - Upload Files
      </h1>

      <div className="bg-white p-6 rounded-xl shadow-md w-full max-w-2xl space-y-6">
        <FileUpload
          label="Select Resumes (Multiple)"
          multiple={true}
          onFileChange={setResumes}
        />
        <FileUpload
          label="Select Job Description"
          multiple={false}
          onFileChange={(file) => setJobDescription(file[0])}
        />
      </div>

      <button
        onClick={handleSubmit}
        disabled={resumes.length === 0 || !jobDescription}
        className="mt-8 px-6 py-3 bg-blue-500 text-white rounded-xl shadow-md hover:bg-blue-600 disabled:opacity-50"
      >
        Submit
      </button>

      {topMatches.length > 0 && (
        <div className="mt-8 w-full max-w-2xl">
          <h2 className="text-xl font-semibold mb-4 text-gray-800">
            Top Matches
          </h2>
          <div className="overflow-x-auto">
            <table className="min-w-full bg-white rounded-xl shadow-md">
              <thead>
                <tr className="bg-gray-200 text-gray-700">
                  <th className="px-4 py-2 text-left">Filename</th>
                  <th className="px-4 py-2 text-left">Similarity</th>
                </tr>
              </thead>
              <tbody>
                {topMatches.map((match, idx) => (
                  <tr key={idx} className="border-t">
                    <td className="px-4 py-2">{match.filename}</td>
                    <td className="px-4 py-2">{match.similarity.toFixed(2)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
