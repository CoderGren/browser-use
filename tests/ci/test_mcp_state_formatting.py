from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from browser_use.mcp.server import BrowserUseServer


@dataclass
class FakeNode:
	tag_name: str
	text: str = ''
	attributes: dict[str, str] = field(default_factory=dict)
	children_nodes: list['FakeNode'] = field(default_factory=list)
	parent_node: 'FakeNode | None' = None
	shadow_roots: list['FakeNode'] = field(default_factory=list)
	absolute_position: Any = None

	def __post_init__(self) -> None:
		for child in self.children_nodes:
			child.parent_node = self
		for shadow_root in self.shadow_roots:
			shadow_root.parent_node = self

	def get_all_children_text(self, max_depth: int = -1) -> str:
		parts = [self.text] if self.text else []

		def collect(node: FakeNode, current_depth: int) -> None:
			if max_depth != -1 and current_depth > max_depth:
				return
			for child in node.children_nodes:
				if child.text:
					parts.append(child.text)
				collect(child, current_depth + 1)

		collect(self, 0)
		return ' '.join(parts)


def test_mcp_element_format_includes_associated_label() -> None:
	server = BrowserUseServer()
	input_node = FakeNode('input', attributes={'id': 'email', 'type': 'email'})
	root = FakeNode(
		'form',
		children_nodes=[
			FakeNode('label', text='Email Address', attributes={'for': 'email'}),
			input_node,
		],
	)
	input_node.parent_node = root

	element = server._format_interactive_element(1, input_node)

	assert element['label'] == 'Email Address'
	assert element['type'] == 'email'
	assert element['id'] == 'email'


def test_mcp_element_format_uses_nearby_preceding_text_for_custom_forms() -> None:
	server = BrowserUseServer()
	input_node = FakeNode('input', attributes={'placeholder': '$'})
	field_group = FakeNode(
		'div',
		children_nodes=[
			FakeNode('div', text='What is the price of the home?'),
			input_node,
		],
	)
	input_node.parent_node = field_group

	element = server._format_interactive_element(2, input_node)

	assert element['label'] == 'What is the price of the home?'
	assert element['placeholder'] == '$'


def test_mcp_element_format_includes_dropdown_state_metadata() -> None:
	server = BrowserUseServer()
	dropdown = FakeNode(
		'div',
		text='Purchase a Home',
		attributes={'role': 'combobox', 'aria-expanded': 'true', 'aria-label': 'Loan purpose'},
	)

	element = server._format_interactive_element(3, dropdown)

	assert element['label'] == 'Loan purpose'
	assert element['role'] == 'combobox'
	assert element['expanded'] == 'true'
	assert element['text'] == 'Purchase a Home'


def test_mcp_element_format_does_not_emit_password_values() -> None:
	server = BrowserUseServer()
	password = FakeNode('input', attributes={'type': 'password', 'value': 'super-secret', 'name': 'password'})

	element = server._format_interactive_element(4, password)

	assert element['label'] == 'password'
	assert 'value' not in element


def test_mcp_element_format_does_not_infer_sibling_label_for_text_button() -> None:
	server = BrowserUseServer()
	next_button = FakeNode('button', text='Next')
	root = FakeNode(
		'div',
		children_nodes=[
			FakeNode('button', text='Save'),
			next_button,
		],
	)
	next_button.parent_node = root

	element = server._format_interactive_element(5, next_button)

	assert element['text'] == 'Next'
	assert 'label' not in element
