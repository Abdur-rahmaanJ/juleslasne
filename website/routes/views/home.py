"""
    Source of juleslasne.com/.net/.me/.fr
    Copyright (C) 2018-2019 Jules Lasne - <jules@juleslasne.com>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from flask import Blueprint, render_template, request, flash, redirect, url_for

from validate_email import validate_email

from website.utils.string import decode_bytes
from website.email.contact import contact_send_mail

home_bp = Blueprint('home', __name__)


@home_bp.route('/')
def home():
    return render_template('index.html')


@home_bp.route('/send_contact_email', methods=["POST", "GET"])
def send_contact_email():
    """`
        Reads the url parameters and sends an email
    """
    name = decode_bytes(request.args.get('contact_name'))
    email = decode_bytes(request.args.get('contact_email'))
    text = decode_bytes(request.args.get('contact_text'))
    copy = bool(request.args.get('copy'))

    if not validate_email(email):
        flash("Sorry, but the email you provided doesn't match the rfc5322 standard.", "error")
        return redirect(url_for("home.home"))
    if email is None:
        flash("Missing email parameter", "error")
        return redirect(url_for("home.home"))
    if text is None:
        flash("Missing text parameter", "error")
        return redirect(url_for("home.home"))
    contact_send_mail(email, text, name, copy)
    flash("Email sent ! I'll get back to you shortly !", "success")
    return redirect(url_for("home.home"))
