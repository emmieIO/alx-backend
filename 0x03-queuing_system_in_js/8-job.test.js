import { expect } from "chai";
import kue from "kue";
import createPushNotificationsJobs from "./8-job.js";

describe("createPushNotificationsJobs", () => {
  let queue;

  beforeEach(() => {
    queue = kue.createQueue();
    kue.Job.rangeByType(
      "push_notification_code_3",
      "inactive",
      0,
      -1,
      "asc",
      (err, selectedJobs) => {
        selectedJobs.forEach((job) => job.remove());
      }
    );
    queue.testMode.enter();
  });

  afterEach(() => {
    queue.testMode.clear();
    queue.testMode.exit();
  });

  it("should display an error message if jobs is not an array", () => {
    expect(() => createPushNotificationsJobs("not an array", queue)).to.throw(
      "Jobs is not an array"
    );
  });

  it("should create two new jobs to the queue", () => {
    const jobs = [
      {
        phoneNumber: "1234567890",
        message: "This is the code 1234 to verify your account",
      },
      {
        phoneNumber: "0987654321",
        message: "This is the code 4321 to verify your account",
      },
    ];

    createPushNotificationsJobs(jobs, queue);
    expect(queue.testMode.jobs.length).to.equal(2);

    expect(queue.testMode.jobs[0].type).to.equal("push_notification_code_3");
    expect(queue.testMode.jobs[0].data).to.deep.equal(jobs[0]);

    expect(queue.testMode.jobs[1].type).to.equal("push_notification_code_3");
    expect(queue.testMode.jobs[1].data).to.deep.equal(jobs[1]);
  });

  it("should log job events to the console", (done) => {
    const jobs = [
      {
        phoneNumber: "1234567890",
        message: "This is the code 1234 to verify your account",
      },
    ];

    const log = console.log;
    const logs = [];
    console.log = (message) => logs.push(message);

    createPushNotificationsJobs(jobs, queue);

    queue.testMode.jobs[0].emit("complete");
    queue.testMode.jobs[0].emit("failed", new Error("Some error"));
    queue.testMode.jobs[0].emit("progress", 50);

    expect(logs).to.include("Notification job created: 1");
    expect(logs).to.include("Notification job 1 completed");
    expect(logs).to.include("Notification job 1 failed: Error: Some error");
    expect(logs).to.include("Notification job 1 50% complete");

    console.log = log;
    done();
  });
});
