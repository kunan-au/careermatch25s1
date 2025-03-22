import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Avatar, AvatarImage, AvatarFallback } from "@/components/ui/avatar";
import { Card, CardContent } from "@/components/ui/card";

const fakeConnections = [
  { name: "Alice Johnson", title: "Frontend Developer at Google" },
  { name: "Michael Lee", title: "Product Manager at Canva" },
  { name: "Emily Chen", title: "Backend Engineer at Amazon" },
  { name: "John Smith", title: "DevOps Engineer at Atlassian" },
  { name: "Sophia Davis", title: "Software Engineer at Adobe" },
  { name: "Daniel Kim", title: "AI Researcher at OpenAI" },
];

const suggestedConnections = [
  { name: "Sara Kim", title: "UI/UX Designer at Atlassian" },
  { name: "David Park", title: "Data Scientist at Amazon" },
  { name: "Liam Nguyen", title: "Machine Learning Engineer at Tesla" },
  { name: "Chloe Williams", title: "Cloud Architect at Microsoft" },
  { name: "Noah Zhang", title: "Cybersecurity Analyst at IBM" },
  { name: "Olivia Brown", title: "Product Designer at Spotify" },
];

export default function MyNetwork() {
  const [connected, setConnected] = useState<string[]>([]);

  const handleConnect = (name: string) => {
    if (!connected.includes(name)) {
      setConnected((prev) => [...prev, name]);
    }
  };

  return (
    <>
      <h1 className="w-full text-center text-3xl font-bold py-10 bg-gray-50">
        My Network
      </h1>

      <div className="bg-gray-50 pb-10 px-4 lg:px-40">
        {/* Connections */}
        <section className="mb-10">
          <h2 className="text-2xl font-semibold mb-4">Your Connections</h2>
          <div className="grid gap-4 sm:grid-cols-2">
            {fakeConnections.map((user, index) => (
              <Card key={index}>
                <CardContent className="flex justify-between items-center p-4">
                  <div className="flex items-center gap-x-6">
                    <Avatar>
                      <AvatarImage src={`https://i.pravatar.cc/80?u=${user.name}`} />
                      <AvatarFallback>{user.name.charAt(0)}</AvatarFallback>
                    </Avatar>
                    <div className="flex flex-col">
                      <span className="font-medium">{user.name}</span>
                      <span className="text-muted-foreground text-sm">{user.title}</span>
                    </div>
                  </div>
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => {
                      console.log(`Message ${user.name}`);
                    }}
                  >
                    Message
                  </Button>
                </CardContent>
              </Card>
            ))}
          </div>
        </section>

        {/* Suggestions */}
        <section>
          <h2 className="text-2xl font-semibold mb-4">People You May Know</h2>
          <div className="grid gap-4 sm:grid-cols-2">
            {suggestedConnections.map((user, index) => {
              const isConnected = connected.includes(user.name);
              return (
                <Card key={index}>
                  <CardContent className="flex justify-between items-center p-4">
                    <div className="flex items-center gap-x-6">
                      <Avatar>
                        <AvatarImage src={`https://i.pravatar.cc/80?u=${user.name}`} />
                        <AvatarFallback>{user.name.charAt(0)}</AvatarFallback>
                      </Avatar>
                      <div className="flex flex-col">
                        <span className="font-medium">{user.name}</span>
                        <span className="text-muted-foreground text-sm">{user.title}</span>
                      </div>
                    </div>
                    <Button
                      size="sm"
                      disabled={isConnected}
                      onClick={() => handleConnect(user.name)}
                    >
                      {isConnected ? "Connected" : "Connect"}
                    </Button>
                  </CardContent>
                </Card>
              );
            })}
          </div>
        </section>
      </div>
    </>
  );
}
