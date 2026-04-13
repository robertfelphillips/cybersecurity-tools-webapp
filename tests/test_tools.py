import socket
import unittest
from unittest.mock import patch

from app.app import app
from app.tools.base64_tool import decode_base64, encode_base64
from app.tools.hash_generator import generate_hash
from app.tools.log_parser import parse_logs
from app.tools.port_scanner import scan_ports


class ToolTests(unittest.TestCase):
    def test_hash_generator_sha256(self):
        self.assertEqual(
            generate_hash("hello", "sha256"),
            "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824",
        )

    def test_base64_round_trip(self):
        encoded = encode_base64("hello")
        self.assertEqual(encoded, "aGVsbG8=")
        self.assertEqual(decode_base64(encoded), "hello")

    def test_invalid_base64_raises_value_error(self):
        with self.assertRaises(ValueError):
            decode_base64("not valid base64!")

    def test_log_parser_counts_security_events(self):
        report = parse_logs(
            "\n".join(
                [
                    "Failed password for invalid user admin from 192.168.1.25 port 55231 ssh2",
                    '10.0.0.8 - - "GET /login HTTP/1.1" 401 512',
                    "app: ERROR database connection denied for user app_user",
                    "firewall: WARNING blocked connection from 8.8.8.8 to port 22",
                ]
            )
        )

        self.assertEqual(report["line_count"], 4)
        self.assertEqual(report["unique_ip_count"], 3)
        self.assertEqual(report["failed_logins"], 1)
        self.assertEqual(report["errors"], 1)
        self.assertEqual(report["warnings"], 1)
        self.assertIn({"status": "401", "count": 1}, report["http_statuses"])

    def test_log_parser_requires_text(self):
        with self.assertRaises(ValueError):
            parse_logs("")

    @patch("app.tools.port_scanner.socket.getaddrinfo", return_value=[object()])
    @patch("app.tools.port_scanner.socket.create_connection")
    def test_port_scanner_reports_open_port(self, mock_create_connection, _):
        mock_create_connection.return_value.__enter__.return_value = object()

        results = scan_ports("127.0.0.1", "80", "80")

        self.assertEqual(results, [{"port": 80, "status": "open", "detail": "Connection accepted"}])

    @patch("app.tools.port_scanner.socket.getaddrinfo", return_value=[object()])
    @patch("app.tools.port_scanner.socket.create_connection")
    def test_port_scanner_reports_closed_port(self, mock_create_connection, _):
        mock_create_connection.side_effect = ConnectionRefusedError()

        results = scan_ports("127.0.0.1", "81", "81")

        self.assertEqual(results, [{"port": 81, "status": "closed", "detail": "Connection refused"}])

    def test_port_scanner_rejects_large_ranges(self):
        with self.assertRaises(ValueError):
            scan_ports("127.0.0.1", "1", "101")


class RouteTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_pages_load(self):
        for path in ["/", "/base64", "/port-scanner", "/log-parser"]:
            with self.subTest(path=path):
                self.assertEqual(self.client.get(path).status_code, 200)

    def test_hash_post(self):
        response = self.client.post("/", data={"input_text": "hello", "algorithm": "sha256"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824", response.data)

    def test_base64_post(self):
        response = self.client.post("/base64", data={"input_text": "hello", "action": "encode"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"aGVsbG8=", response.data)

    def test_log_parser_post(self):
        response = self.client.post(
            "/log-parser",
            data={"log_text": "Failed password from 192.168.1.25"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Failed logins", response.data)

    def test_port_scanner_requires_permission(self):
        response = self.client.post(
            "/port-scanner",
            data={"host": "127.0.0.1", "start_port": "1", "end_port": "3"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Confirm you have permission", response.data)


if __name__ == "__main__":
    unittest.main()
