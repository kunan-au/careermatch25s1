import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

const fakeConnections = [
  { name: "Alice Johnson", title: "Frontend Developer at Google" },
  { name: "Michael Lee", title: "Product Manager at Canva" },
];

const suggestedConnections = [
  { name: "Sara Kim", title: "UI/UX Designer at Atlassian" },
  { name: "David Park", title: "Data Scientist at Amazon" },
];

export default function MyNetwork() {
  return (
    <>
      <h1 className="w-full text-center text-3xl font-bold py-10 bg-gray-50">
        My Network
      </h1>

      <div className="bg-gray-50 pb-10 px-4 lg:px-40">
        <section className="mb-10">
          <h2 className="text-2xl font-semibold mb-4">Your Connections</h2>
          <div className="grid gap-4 sm:grid-cols-2">
            {fakeConnections.map((user, index) => (
              <Card key={index}>
                <CardHeader>
                  <CardTitle>{user.name}</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-muted-foreground mb-2">{user.title}</p>
                  <Button variant="outline">Message</Button>
                </CardContent>
              </Card>
            ))}
          </div>
        </section>

        <section>
          <h2 className="text-2xl font-semibold mb-4">People You May Know</h2>
          <div className="grid gap-4 sm:grid-cols-2">
            {suggestedConnections.map((user, index) => (
              <Card key={index}>
                <CardHeader>
                  <CardTitle>{user.name}</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-muted-foreground mb-2">{user.title}</p>
                  <Button>Add Connection</Button>
                </CardContent>
              </Card>
            ))}
          </div>
        </section>
      </div>
    </>
  );
}
