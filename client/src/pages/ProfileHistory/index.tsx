export default function ProfileHistory() {
    /*A page for history */
    return (
        <div className="text-center bg-gray-50">
            <h1 className="w-full text-center text-3xl font-bold py-10">
                Your Application History
            </h1>
            <ul className="space-y-4 max-w-4xl mx-auto text-left">
                <li className="bg-white shadow rounded-lg p-6 border">
                    <div className="flex justify-between items-center">
                        <div>
                            <h3 className="font-bold mt-px">Frontend Developer at TechCorp</h3>
                            <p className="text-sm text-gray-500">Applied on March 25, 2025</p>
                        </div>
                        <span className="text-sm font-medium text-green-600 bg-green-100 px-3 py-1 rounded-full">
                            Under Review
                        </span>
                    </div>
                </li>
                <li className="bg-white shadow rounded-lg p-6 border">
                    <div className="flex justify-between items-center">
                        <div>
                            <h3 className="font-bold mt-px">UX Designer at CreateLab</h3>
                            <p className="text-sm text-gray-500">Applied on February 12, 2025</p>
                        </div>
                        <span className="text-sm font-medium text-red-600 bg-red-100 px-3 py-1 rounded-full">
                            Rejected
                        </span>
                    </div>
                </li>
                <li className="bg-white shadow rounded-lg p-6 border">
                    <div className="flex justify-between items-center">
                        <div>
                            <h3 className="font-bold mt-px">Software Engineer at DevSolutions</h3>
                            <p className="text-sm text-gray-500">Applied on January 30, 2025</p>
                        </div>
                        <span className="text-sm font-medium text-blue-600 bg-blue-100 px-3 py-1 rounded-full">
                            Interview Scheduled
                        </span>
                    </div>
                </li>
            </ul>
            <br />
        </div>
    );
}
