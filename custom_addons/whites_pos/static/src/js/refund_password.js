odoo.define("whites_pos.RefundPasswordButton", function (require) {
    "use strict";

    const Registries = require("point_of_sale.Registries");
    const TicketScreen = require("point_of_sale.TicketScreen");
    const rpc = require("web.rpc");

    const RefundPassword = (TicketScreen) => class extends TicketScreen {
        async _onDoRefund() {
            // Prompt password before approving refund
            const order = this.getSelectedSyncedOrder();
            if (!order) {
                this._state.ui.highlightHeaderNote = !this._state.ui.highlightHeaderNote;
                return this.render();
            }

            const customer = order.get_client();
            const allToRefundDetails = this._getRefundableDetails(customer)
            if (allToRefundDetails.length == 0) {
                this._state.ui.highlightHeaderNote = !this._state.ui.highlightHeaderNote;
                return this.render();
            }

            let refund = await rpc.query({
                model: "hr.employee",
                method: "get_password_refund",
                args: [this.env.pos.employee.user_id[0]],
            });

            const { confirmed, payload } = await this.showPopup("NumberPopup", {
                isPassword: true,
                title: this.env._t('Password ?'),
                startingValue: null,
            });

            if (!confirmed) return false;

            if (refund == payload) {
                super._onDoRefund();
            } else {
                this.showPopup("ErrorPopup", {
                    body: this.env._t("Incorrect Password"),
                });
            }
        }
    };

    Registries.Component.extend(TicketScreen, RefundPassword);
});
