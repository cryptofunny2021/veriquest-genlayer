# v0.2.16
# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }

from genlayer import *


class VeriQuest(gl.Contract):

    quest_title: str
    quest_description: str
    quest_category: str

    last_submission: str
    last_result: str

    submission_count: u256

    best_score: u256
    best_result: str

    total_score: u256
    evaluation_count: u256

    last_reward_tier: str

    highest_reward_score: u256
    highest_reward_tier: str

    last_category: str

    winning_submission: str
    winning_score: u256

    campaign_status: str
    campaign_decision: str

    reputation_score: u256

    successful_submissions: u256
    failed_submissions: u256

    gold_rewards: u256
    silver_rewards: u256

    def __init__(self):

        self.quest_title = ""
        self.quest_description = ""
        self.quest_category = "Education"

        self.last_submission = ""
        self.last_result = ""

        self.submission_count = u256(0)

        self.best_score = u256(0)
        self.best_result = ""

        self.total_score = u256(0)
        self.evaluation_count = u256(0)

        self.last_reward_tier = "None"

        self.highest_reward_score = u256(0)
        self.highest_reward_tier = "None"

        self.last_category = ""

        self.winning_submission = ""
        self.winning_score = u256(0)

        self.campaign_status = "Pending"
        self.campaign_decision = "No Decision"

        self.reputation_score = u256(0)

        self.successful_submissions = u256(0)
        self.failed_submissions = u256(0)

        self.gold_rewards = u256(0)
        self.silver_rewards = u256(0)

    @gl.public.write
    def create_quest(
        self,
        title: str,
        description: str,
        category: str
    ) -> None:

        self.quest_title = title
        self.quest_description = description
        self.quest_category = category

    @gl.public.write
    def submit_content(
        self,
        content: str
    ) -> None:

        self.last_submission = content
        self.last_category = self.quest_category

        evaluation_criteria = ""

        if self.quest_category == "Education":

            evaluation_criteria = """
Evaluate:
- Accuracy
- Educational Value
- Clarity
"""

        elif self.quest_category == "Marketing":

            evaluation_criteria = """
Evaluate:
- Engagement
- Creativity
- Call-To-Action
"""

        elif self.quest_category == "Research":

            evaluation_criteria = """
Evaluate:
- Evidence
- Depth
- Reasoning
"""

        else:

            evaluation_criteria = """
Evaluate:
- Helpfulness
- Impact
- Contribution
"""

        prompt_input = f"""
Quest Title:
{self.quest_title}

Quest Description:
{self.quest_description}

Quest Category:
{self.quest_category}

Submitted Content:
{content}
"""

        result = gl.eq_principle.prompt_non_comparative(
            lambda: prompt_input,
            task="""
Evaluate the submitted content.

Return exactly:

Score: <number>
Reason: <short reason>

The score must be between 0 and 100.
""",
            criteria=evaluation_criteria
        )

        self.last_result = result
        self.submission_count += u256(1)

        try:

            score_text = result.split("Score:")[1].split("\n")[0].strip()
            score_value = u256(int(score_text))

            if score_value > self.winning_score:

                self.winning_score = score_value
                self.winning_submission = content

            self.total_score += score_value
            self.evaluation_count += u256(1)

            if score_value > self.best_score:
                self.best_score = score_value
                self.best_result = result

            if score_value >= u256(80):

                self.last_reward_tier = "Gold"

                self.reputation_score += u256(10)
                self.successful_submissions += u256(1)
                self.gold_rewards += u256(1)

                if score_value > self.highest_reward_score:
                    self.highest_reward_score = score_value
                    self.highest_reward_tier = "Gold"

            elif score_value >= u256(40):

                self.last_reward_tier = "Silver"

                self.reputation_score += u256(5)
                self.successful_submissions += u256(1)
                self.silver_rewards += u256(1)

                if score_value > self.highest_reward_score:
                    self.highest_reward_score = score_value
                    self.highest_reward_tier = "Silver"

            else:

                self.last_reward_tier = "Rejected"

                self.failed_submissions += u256(1)

                if self.reputation_score >= u256(2):
                    self.reputation_score -= u256(2)

            if self.winning_score >= u256(80):

                self.campaign_status = "Approved"

                self.campaign_decision = (
                    "High quality content approved by AI evaluation."
                )

            elif self.winning_score >= u256(40):

                self.campaign_status = "Review"

                self.campaign_decision = (
                    "Content requires additional review."
                )

            else:

                self.campaign_status = "Rejected"

                self.campaign_decision = (
                    "Content quality below acceptance threshold."
                )

        except:
            pass

    @gl.public.view
    def get_quest(self) -> str:

        return (
            "Title: "
            + self.quest_title
            + "\n\nDescription: "
            + self.quest_description
        )

    @gl.public.view
    def get_category(self) -> str:
        return self.quest_category

    @gl.public.view
    def get_last_result(self) -> str:
        return self.last_result

    @gl.public.view
    def get_last_submission(self) -> str:
        return self.last_submission

    @gl.public.view
    def get_submission_count(self) -> u256:
        return self.submission_count

    @gl.public.view
    def get_best_score(self) -> u256:
        return self.best_score

    @gl.public.view
    def get_best_result(self) -> str:
        return self.best_result

    @gl.public.view
    def get_my_score(self) -> u256:

        if self.evaluation_count == u256(0):
            return u256(0)

        return self.total_score // self.evaluation_count

    @gl.public.view
    def get_my_evaluation_count(self) -> u256:
        return self.evaluation_count

    @gl.public.view
    def get_reward_tier(self) -> str:
        return self.last_reward_tier

    @gl.public.view
    def get_highest_reward_score(self) -> u256:
        return self.highest_reward_score

    @gl.public.view
    def get_highest_reward_tier(self) -> str:
        return self.highest_reward_tier

    @gl.public.view
    def get_average_score(self) -> u256:

        if self.evaluation_count == u256(0):
            return u256(0)

        return self.total_score // self.evaluation_count

    @gl.public.view
    def get_winning_score(self) -> u256:
        return self.winning_score

    @gl.public.view
    def get_winning_submission(self) -> str:
        return self.winning_submission

    @gl.public.view
    def get_campaign_status(self) -> str:
        return self.campaign_status

    @gl.public.view
    def get_campaign_decision(self) -> str:
        return self.campaign_decision

    @gl.public.view
    def get_reputation_score(self) -> u256:
        return self.reputation_score

    @gl.public.view
    def get_successful_submissions(self) -> u256:
        return self.successful_submissions

    @gl.public.view
    def get_failed_submissions(self) -> u256:
        return self.failed_submissions

    @gl.public.view
    def get_gold_rewards(self) -> u256:
        return self.gold_rewards

    @gl.public.view
    def get_silver_rewards(self) -> u256:
        return self.silver_rewards

    @gl.public.view
    def get_reputation_profile(self) -> str:

        status = "New Contributor"

        if self.reputation_score >= u256(50):
            status = "Trusted Contributor"

        elif self.reputation_score >= u256(20):
            status = "Active Contributor"

        return (
            "Reputation Score: "
            + str(int(self.reputation_score))
            + "\n\nSuccessful Submissions: "
            + str(int(self.successful_submissions))
            + "\n\nFailed Submissions: "
            + str(int(self.failed_submissions))
            + "\n\nGold Rewards: "
            + str(int(self.gold_rewards))
            + "\n\nSilver Rewards: "
            + str(int(self.silver_rewards))
            + "\n\nStatus: "
            + status
        )

    @gl.public.view
    def get_campaign_summary(self) -> str:

        average_score = 0

        if self.evaluation_count > u256(0):
            average_score = int(
                self.total_score // self.evaluation_count
            )

        return (
            "Quest: "
            + self.quest_title
            + "\n\nCategory: "
            + self.last_category
            + "\n\nSubmissions: "
            + str(int(self.submission_count))
            + "\n\nAverage Score: "
            + str(average_score)
            + "\n\nBest Score: "
            + str(int(self.best_score))
            + "\n\nHighest Reward Tier: "
            + self.highest_reward_tier
            + "\n\nWinning Score: "
            + str(int(self.winning_score))
            + "\n\nCampaign Status: "
            + self.campaign_status
        )
