# Copyright 2026 Domatix <https://www.domatix.cloud>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models


class SocialPost(models.Model):
    """TikTok requirements on the posts to publish."""

    _inherit = "social.post"

    def _get_post_errors(self, media_type, account=None):
        """TikTok publishes videos only, so a post without one is rejected."""
        errors = super()._get_post_errors(media_type, account=account)
        if media_type == "tiktok" and not self.video_ids:
            errors.append(
                self.env._(
                    "TikTok only supports video posts. Please add a video "
                    "or remove the TikTok accounts from this post."
                )
            )
        return errors

    @api.depends("account_ids", "image_ids", "video_ids")
    def _compute_message_info(self):
        res = super()._compute_message_info()
        for post in self:
            if (
                post.image_ids
                and post.video_ids
                and "tiktok" in post.account_ids.mapped("media_type")
            ):
                message_info = self.env._(
                    "You have selected images and videos for this post. "
                    "TikTok only publishes videos, so the images will be ignored."
                )
                post.message_info = (
                    f"{post.message_info}\n{message_info}"
                    if post.message_info
                    else message_info
                )
        return res
