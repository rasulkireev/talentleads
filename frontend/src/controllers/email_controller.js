import { Controller } from "@hotwired/stimulus";

export default class extends Controller {
  static targets = ["emailTemplate", "sendEmailLink", "profileId"];

  connect() {
    this.updateSendEmail();
    this.emailTemplateTarget.addEventListener("change", this.updateSendEmail.bind(this));
  }

  updateSendEmail() {
    let profileId = this.profileIdTarget.value;
    let selectedOptionId = this.emailTemplateTarget.value;
    let sendEmailLink = this.sendEmailLinkTarget;

    sendEmailLink.href = `${profileId}/send/${selectedOptionId}`;
  }
}